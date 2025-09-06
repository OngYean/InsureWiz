"""
Policy comparison service with scoring and LangChain analysis
"""

import logging
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime
import uuid

from ..models.policy import PolicyRecord
from ..models.customer import CustomerInput, ComparisonRequest
from ..models.comparison import (
    ComparisonResult, PolicyRecommendation, PolicyScore, 
    ComparisonSummary, ComparisonMatrix
)
from ..chains.analysis import analysis_chain, comparison_chain
from ..utils.simple_scoring_v2 import PolicyScorer
from ..database.operations import policy_ops, comparison_ops

logger = logging.getLogger(__name__)

class PolicyComparator:
    """Main service for comparing insurance policies"""
    
    def __init__(self):
        self.scorer = PolicyScorer()
        self.analysis_chain = analysis_chain
        self.comparison_chain = comparison_chain
    
    async def compare_policies(self, request: ComparisonRequest) -> ComparisonResult:
        """Compare policies for a customer and return ranked recommendations"""
        session_id = str(uuid.uuid4())
        start_time = datetime.now()
        
        try:
            logger.info(f"Starting comparison session {session_id}")
            
            # Get eligible policies
            policies = await self._get_eligible_policies(request)
            
            if not policies:
                logger.warning("No eligible policies found")
                return self._create_empty_result(session_id, request.customer)
            
            logger.info(f"Found {len(policies)} eligible policies")
            
            # Score and rank policies
            scored_policies = await self._score_policies(policies, request.customer)
            
            # Generate AI analysis for top policies
            recommendations = await self._generate_recommendations(
                scored_policies[:request.max_results], 
                request.customer
            )
            
            # Create comparison matrix
            matrix = self._create_comparison_matrix(scored_policies)
            
            # Generate summary
            summary = self._create_comparison_summary(scored_policies, request.customer)
            
            # Get market insights from LangChain
            market_analysis = await self._get_market_insights(policies, request.customer)
            
            # Create final result
            result = ComparisonResult(
                session_id=session_id,
                customer_name=request.customer.name,
                comparison_date=datetime.now(),
                recommendations=recommendations,
                summary=summary,
                matrix=matrix,
                market_insights=market_analysis.get("market_insights", []),
                general_recommendations=market_analysis.get("general_recommendations", []),
                next_steps=market_analysis.get("next_steps", []),
                data_sources=self._get_data_sources(policies),
                disclaimer=self._get_disclaimer(),
                compliance_notes=self._get_compliance_notes(),
                processing_time=(datetime.now() - start_time).total_seconds(),
                ai_model_used="gemini-2.0-flash",
                data_freshness=self._get_data_freshness(policies)
            )
            
            # Save comparison result
            await comparison_ops.save_comparison(result)
            
            logger.info(f"Comparison completed: {session_id}")
            return result
            
        except Exception as e:
            logger.error(f"Error in policy comparison: {e}")
            raise
    
    async def _get_eligible_policies(self, request: ComparisonRequest) -> List[PolicyRecord]:
        """Get policies that match customer criteria"""
        # Get all policies
        all_policies = await policy_ops.get_policies(limit=200)
        
        # Filter by customer preferences
        eligible_policies = []
        
        for policy in all_policies:
            if self._is_policy_eligible(policy, request.customer):
                eligible_policies.append(policy)
        
        return eligible_policies
    
    def _is_policy_eligible(self, policy: PolicyRecord, customer: CustomerInput) -> bool:
        """Check if policy is eligible for customer"""
        # Check Takaful preference
        if customer.preferences.takaful_preference and not policy.is_takaful:
            return False
        
        # Check excluded insurers
        if policy.insurer in customer.preferences.excluded_insurers:
            return False
        
        # Check vehicle age eligibility
        vehicle_age = datetime.now().year - customer.vehicle.year
        
        if policy.eligibility.max_vehicle_age is not None:
            if vehicle_age > policy.eligibility.max_vehicle_age:
                return False
        
        if policy.eligibility.min_vehicle_age is not None:
            if vehicle_age < policy.eligibility.min_vehicle_age:
                return False
        
        # Check driver age eligibility
        if policy.eligibility.max_driver_age is not None:
            if customer.driver.age > policy.eligibility.max_driver_age:
                return False
        
        if policy.eligibility.min_driver_age is not None:
            if customer.driver.age < policy.eligibility.min_driver_age:
                return False
        
        # Check license years
        if policy.eligibility.min_license_years is not None:
            if customer.driver.license_years < policy.eligibility.min_license_years:
                return False
        
        return True
    
    async def _score_policies(self, policies: List[PolicyRecord], customer: CustomerInput) -> List[Tuple[PolicyRecord, PolicyScore]]:
        """Score and rank policies"""
        scored_policies = []
        
        for policy in policies:
            try:
                score = self.scorer.score_policy(policy, customer)
                scored_policies.append((policy, score))
                
            except Exception as e:
                logger.error(f"Error scoring policy {policy.product_name}: {e}")
                continue
        
        # Sort by total score (descending)
        scored_policies.sort(key=lambda x: x[1].total_score, reverse=True)
        
        return scored_policies
    
    async def _generate_recommendations(self, scored_policies: List[Tuple[PolicyRecord, PolicyScore]], customer: CustomerInput) -> List[PolicyRecommendation]:
        """Generate detailed recommendations with AI analysis"""
        recommendations = []
        
        for rank, (policy, score) in enumerate(scored_policies, 1):
            try:
                # Get AI analysis for this policy
                analysis = self.analysis_chain.analyze_policy(policy, customer)
                
                # Create recommendation
                recommendation = PolicyRecommendation(
                    policy=policy,
                    rank=rank,
                    score=score,
                    strengths=analysis.get("strengths", []),
                    weaknesses=analysis.get("weaknesses", []),
                    best_for=analysis.get("best_for", []),
                    key_features=analysis.get("key_features", []),
                    coverage_analysis=analysis.get("coverage_analysis", ""),
                    service_analysis=analysis.get("service_analysis", ""),
                    value_analysis=analysis.get("value_analysis", ""),
                    eligibility_notes=self._get_eligibility_notes(policy, customer),
                    exclusion_warnings=self._get_exclusion_warnings(policy)
                )
                
                recommendations.append(recommendation)
                
            except Exception as e:
                logger.error(f"Error generating recommendation for {policy.product_name}: {e}")
                continue
        
        return recommendations
    
    def _create_comparison_matrix(self, scored_policies: List[Tuple[PolicyRecord, PolicyScore]]) -> ComparisonMatrix:
        """Create feature comparison matrix"""
        insurers = [policy.insurer for policy, _ in scored_policies]
        
        # Define features to compare
        features = [
            "Coverage Type", "Takaful", "Flood Coverage", "Theft Coverage",
            "Windscreen", "Personal Accident", "24/7 Roadside", "Digital Claims",
            "Mobile App", "NCD Protection", "Key Replacement", "Courtesy Car"
        ]
        
        # Build matrix
        matrix = {}
        best_coverage = None
        best_service = None
        best_value = None
        highest_score = 0
        
        for policy, score in scored_policies:
            insurer = policy.insurer
            matrix[insurer] = {}
            
            # Basic info
            matrix[insurer]["Coverage Type"] = policy.coverage_type
            matrix[insurer]["Takaful"] = "Yes" if policy.is_takaful else "No"
            
            # Coverage features
            matrix[insurer]["Flood Coverage"] = "Yes" if policy.included_cover.flood else "No"
            matrix[insurer]["Theft Coverage"] = "Yes" if policy.included_cover.theft else "No"
            matrix[insurer]["Windscreen"] = "Yes" if policy.included_cover.windscreen else "No"
            matrix[insurer]["Personal Accident"] = "Yes" if policy.included_cover.personal_accident else "No"
            
            # Service features
            matrix[insurer]["24/7 Roadside"] = "Yes" if policy.services.roadside_assist_24_7 else "No"
            matrix[insurer]["Digital Claims"] = "Yes" if policy.services.digital_claims else "No"
            matrix[insurer]["Mobile App"] = "Yes" if policy.services.mobile_app else "No"
            
            # Add-on features
            matrix[insurer]["NCD Protection"] = "Available" if policy.addons.ncd_protection else "No"
            matrix[insurer]["Key Replacement"] = "Available" if policy.addons.key_replacement else "No"
            matrix[insurer]["Courtesy Car"] = "Available" if policy.addons.courtesy_car else "No"
            
            # Track best performers
            if score.coverage_score > 80 and (not best_coverage or score.coverage_score > highest_score):
                best_coverage = insurer
            
            if score.service_score > 80:
                best_service = insurer
            
            if score.total_score > highest_score:
                best_value = insurer
                highest_score = score.total_score
        
        return ComparisonMatrix(
            insurers=insurers,
            features=features,
            matrix=matrix,
            best_coverage=best_coverage,
            best_service=best_service,
            best_value=best_value,
            most_comprehensive=best_value  # For now, same as best value
        )
    
    def _create_comparison_summary(self, scored_policies: List[Tuple[PolicyRecord, PolicyScore]], customer: CustomerInput) -> ComparisonSummary:
        """Create comparison summary"""
        if not scored_policies:
            return ComparisonSummary(
                total_policies_compared=0,
                top_recommendation="No policies found",
                coverage_range={},
                price_indicators={},
                takaful_options=0,
                service_levels={}
            )
        
        top_policy, _ = scored_policies[0]
        
        # Count coverage types
        coverage_range = {}
        for policy, _ in scored_policies:
            coverage_type = policy.coverage_type
            coverage_range[coverage_type] = coverage_range.get(coverage_type, 0) + 1
        
        # Count takaful options
        takaful_count = sum(1 for policy, _ in scored_policies if policy.is_takaful)
        
        # Service level distribution
        service_levels = {
            "24/7 Roadside": sum(1 for policy, _ in scored_policies if policy.services.roadside_assist_24_7),
            "Digital Claims": sum(1 for policy, _ in scored_policies if policy.services.digital_claims),
            "Mobile App": sum(1 for policy, _ in scored_policies if policy.services.mobile_app)
        }
        
        return ComparisonSummary(
            total_policies_compared=len(scored_policies),
            top_recommendation=f"{top_policy.insurer} - {top_policy.product_name}",
            coverage_range=coverage_range,
            price_indicators={"rebates_available": sum(1 for policy, _ in scored_policies if policy.pricing_notes.rebates)},
            takaful_options=takaful_count,
            service_levels=service_levels
        )
    
    async def _get_market_insights(self, policies: List[PolicyRecord], customer: CustomerInput) -> Dict[str, Any]:
        """Get market insights from LangChain"""
        try:
            return self.comparison_chain.compare_policies(policies, customer)
        except Exception as e:
            logger.error(f"Error getting market insights: {e}")
            return {
                "market_insights": ["Market analysis temporarily unavailable"],
                "general_recommendations": ["Please review policy details carefully"],
                "next_steps": ["Contact insurers for detailed quotes"]
            }
    
    def _get_eligibility_notes(self, policy: PolicyRecord, customer: CustomerInput) -> List[str]:
        """Get eligibility-related notes"""
        notes = []
        
        vehicle_age = datetime.now().year - customer.vehicle.year
        
        if policy.eligibility.max_vehicle_age is not None:
            notes.append(f"Maximum vehicle age: {policy.eligibility.max_vehicle_age} years (your vehicle: {vehicle_age} years)")
        
        if policy.eligibility.min_driver_age is not None:
            notes.append(f"Minimum driver age: {policy.eligibility.min_driver_age} years")
        
        if policy.eligibility.min_license_years is not None:
            notes.append(f"Minimum license experience: {policy.eligibility.min_license_years} years")
        
        return notes
    
    def _get_exclusion_warnings(self, policy: PolicyRecord) -> List[str]:
        """Get important exclusion warnings"""
        warnings = []
        
        for exclusion in policy.exclusions:
            if any(keyword in exclusion.lower() for keyword in ['flood', 'act of god', 'war', 'terrorism']):
                warnings.append(exclusion)
        
        return warnings
    
    def _get_data_sources(self, policies: List[PolicyRecord]) -> List[str]:
        """Get all data source URLs"""
        sources = set()
        for policy in policies:
            sources.update(policy.source_urls)
        return list(sources)
    
    def _get_disclaimer(self) -> str:
        """Get legal disclaimer"""
        return (
            "This comparison is based on publicly available information from insurers' official sources. "
            "All policies are subject to underwriting approval and specific terms and conditions. "
            "Prices and coverage may vary based on individual circumstances. "
            "Please verify details directly with insurers before making decisions. "
            "This service complies with BNM guidelines on professionalism of agents and PDPA requirements."
        )
    
    def _get_compliance_notes(self) -> List[str]:
        """Get compliance-related notes"""
        return [
            "Data processing conducted under customer consent (PDPA compliance)",
            "Recommendations based on disclosed customer information and preferences",
            "All policy information sourced from official insurer websites",
            "Comparison methodology follows BNM guidelines for agent professionalism"
        ]
    
    def _get_data_freshness(self, policies: List[PolicyRecord]) -> Dict[str, datetime]:
        """Get data freshness information"""
        freshness = {}
        for policy in policies:
            if policy.last_checked:
                insurer = policy.insurer
                if insurer not in freshness or policy.last_checked > freshness[insurer]:
                    freshness[insurer] = policy.last_checked
        return freshness
    
    def _create_empty_result(self, session_id: str, customer: CustomerInput) -> ComparisonResult:
        """Create empty result when no policies found"""
        return ComparisonResult(
            session_id=session_id,
            customer_name=customer.name,
            comparison_date=datetime.now(),
            recommendations=[],
            summary=ComparisonSummary(
                total_policies_compared=0,
                top_recommendation="No eligible policies found",
                coverage_range={},
                price_indicators={},
                takaful_options=0,
                service_levels={}
            ),
            matrix=ComparisonMatrix(
                insurers=[],
                features=[],
                matrix={}
            ),
            market_insights=["No policies available for comparison"],
            general_recommendations=["Please adjust your criteria and try again"],
            next_steps=["Contact insurers directly for quotes"]
        )

# Global instance
policy_comparator = PolicyComparator()
