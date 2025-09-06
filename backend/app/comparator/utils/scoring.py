"""
Policy scoring system with weighted factors
"""

import logging
from typing import Dict, Any, TYPE_CHECKING
from datetime import datetime
from pydantic import BaseModel, Field

if TYPE_CHECKING:
    from ..models.policy import PolicyRecord

logger = logging.getLogger(__name__)


class ScoreWeights(BaseModel):
    """Configurable weights for policy scoring"""
    coverage_weight: float = Field(default=0.25, description="Coverage breadth weight")
    service_weight: float = Field(default=0.20, description="Service quality weight") 
    takaful_weight: float = Field(default=0.15, description="Takaful preference weight")
    pricing_weight: float = Field(default=0.25, description="Pricing attractiveness weight")
    eligibility_weight: float = Field(default=0.15, description="Eligibility match weight")


class PolicyScore(BaseModel):
    """Individual scoring components for a policy"""
    coverage_score: float = Field(..., description="Coverage breadth score (0-100)")
    service_score: float = Field(..., description="Service quality score (0-100)")
    takaful_score: float = Field(..., description="Takaful preference score (0-100)")
    pricing_score: float = Field(..., description="Pricing attractiveness score (0-100)")
    eligibility_score: float = Field(..., description="Eligibility match score (0-100)")
    total_score: float = Field(..., description="Weighted total score (0-100)")
    
    # Detailed breakdowns
    coverage_details: Dict[str, Any] = Field(default_factory=dict, description="Coverage scoring details")
    service_details: Dict[str, Any] = Field(default_factory=dict, description="Service scoring details")
    pricing_details: Dict[str, Any] = Field(default_factory=dict, description="Pricing scoring details")

class PolicyScorer:
    """Scoring system for insurance policies"""
    
    def __init__(self):
        # Scoring weights (must sum to 1.0)
        self.weights = {
            "coverage": 0.25,      # Coverage breadth
            "service": 0.20,       # Service quality
            "takaful": 0.15,       # Takaful preference match
            "pricing": 0.25,       # Pricing attractiveness
            "eligibility": 0.15    # Eligibility match
        }
    
    def score_policy(self, policy: PolicyRecord, customer: CustomerInput) -> PolicyScore:
        """Score a policy against customer preferences"""
        try:
            # Calculate individual scores
            coverage_score = self._score_coverage(policy, customer)
            service_score = self._score_service(policy, customer)
            takaful_score = self._score_takaful_match(policy, customer)
            pricing_score = self._score_pricing(policy, customer)
            eligibility_score = self._score_eligibility(policy, customer)
            
            # Calculate weighted total
            total_score = (
                coverage_score * self.weights["coverage"] +
                service_score * self.weights["service"] +
                takaful_score * self.weights["takaful"] +
                pricing_score * self.weights["pricing"] +
                eligibility_score * self.weights["eligibility"]
            )
            
            # Create detailed scoring breakdown
            coverage_details = self._get_coverage_details(policy, customer)
            service_details = self._get_service_details(policy, customer)
            pricing_details = self._get_pricing_details(policy, customer)
            
            return PolicyScore(
                coverage_score=coverage_score,
                service_score=service_score,
                takaful_score=takaful_score,
                pricing_score=pricing_score,
                eligibility_score=eligibility_score,
                total_score=total_score,
                coverage_details=coverage_details,
                service_details=service_details,
                pricing_details=pricing_details
            )
            
        except Exception as e:
            logger.error(f"Error scoring policy {policy.product_name}: {e}")
            # Return default score
            return PolicyScore(
                coverage_score=50.0,
                service_score=50.0,
                takaful_score=50.0,
                pricing_score=50.0,
                eligibility_score=50.0,
                total_score=50.0,
                coverage_details={},
                service_details={},
                pricing_details={}
            )
    
    def _score_coverage(self, policy: PolicyRecord, customer: CustomerInput) -> float:
        """Score coverage breadth (0-100)"""
        score = 0.0
        max_score = 100.0
        
        # Base score for coverage type
        if policy.coverage_type == "Comprehensive":
            score += 40.0
        elif policy.coverage_type == "Third Party, Fire & Theft":
            score += 25.0
        else:  # Third Party
            score += 10.0
        
        # Coverage inclusions (each worth points)
        coverage_points = {
            'flood': 8.0,
            'theft': 6.0,
            'riot_strike': 4.0,
            'windscreen': 6.0,
            'personal_accident': 8.0,
            'accessories': 4.0,
            'natural_disaster': 6.0,
            'ehailing_coverage': 8.0,
            'passenger_liability': 5.0,
            'legal_liability': 5.0
        }
        
        for coverage, points in coverage_points.items():
            if getattr(policy.included_cover, coverage, False):
                score += points
        
        # Adjust based on customer priority
        if customer.preferences.coverage_priority == CoveragePriority.PREMIUM:
            # Premium customers want maximum coverage
            score = min(score * 1.1, max_score)
        elif customer.preferences.coverage_priority == CoveragePriority.BASIC:
            # Basic customers may be satisfied with less
            score = min(score * 0.9 + 10, max_score)
        
        return min(score, max_score)
    
    def _score_service(self, policy: PolicyRecord, customer: CustomerInput) -> float:
        """Score service quality (0-100)"""
        score = 0.0
        
        # Service features scoring
        if policy.services.roadside_assist_24_7:
            score += 20.0
        
        if policy.services.claim_fast_track:
            score += 15.0
        
        if policy.services.digital_claims:
            score += 15.0
        
        if policy.services.mobile_app:
            score += 10.0
        
        if policy.services.online_portal:
            score += 10.0
        
        # Panel workshop network
        if policy.services.panel_workshop_count:
            if policy.services.panel_workshop_count >= 100:
                score += 15.0
            elif policy.services.panel_workshop_count >= 50:
                score += 10.0
            else:
                score += 5.0
        
        # SLA response time bonus
        if policy.services.roadside_assist_sla:
            if "30 min" in policy.services.roadside_assist_sla.lower():
                score += 10.0
            elif "60 min" in policy.services.roadside_assist_sla.lower():
                score += 5.0
        
        # Bonus for customer service priorities
        for priority in customer.preferences.service_priorities:
            priority_lower = priority.lower()
            if "digital" in priority_lower and policy.services.digital_claims:
                score += 5.0
            elif "roadside" in priority_lower and policy.services.roadside_assist_24_7:
                score += 5.0
            elif "app" in priority_lower and policy.services.mobile_app:
                score += 5.0
        
        return min(score, 100.0)
    
    def _score_takaful_match(self, policy: PolicyRecord, customer: CustomerInput) -> float:
        """Score Takaful preference match (0-100)"""
        if customer.preferences.takaful_preference:
            return 100.0 if policy.is_takaful else 0.0
        else:
            # Neutral scoring if no preference
            return 50.0
    
    def _score_pricing(self, policy: PolicyRecord, customer: CustomerInput) -> float:
        """Score pricing attractiveness (0-100)"""
        score = 50.0  # Base score
        
        # Rebates and discounts
        if policy.pricing_notes.rebates:
            score += len(policy.pricing_notes.rebates) * 5.0
        
        if policy.pricing_notes.cashback:
            score += len(policy.pricing_notes.cashback) * 5.0
        
        if policy.pricing_notes.bundling_discounts:
            score += len(policy.pricing_notes.bundling_discounts) * 3.0
        
        if policy.pricing_notes.loyalty_benefits:
            score += len(policy.pricing_notes.loyalty_benefits) * 3.0
        
        if policy.pricing_notes.promotional_offers:
            score += len(policy.pricing_notes.promotional_offers) * 4.0
        
        # Young driver considerations
        if customer.driver.age <= 25:
            if "young driver" in policy.product_name.lower() or "graduate" in policy.product_name.lower():
                score += 15.0
        
        # Loyalty customer bonus
        if customer.driver.license_years >= 5:
            if policy.pricing_notes.loyalty_benefits:
                score += 10.0
        
        return min(score, 100.0)
    
    def _score_eligibility(self, policy: PolicyRecord, customer: CustomerInput) -> float:
        """Score eligibility match (0-100)"""
        score = 100.0  # Start with perfect score, deduct for mismatches
        
        vehicle_age = datetime.now().year - customer.vehicle.year
        
        # Vehicle age checks
        if policy.eligibility.max_vehicle_age is not None:
            if vehicle_age > policy.eligibility.max_vehicle_age:
                return 0.0  # Complete mismatch
            elif vehicle_age == policy.eligibility.max_vehicle_age:
                score -= 20.0  # Close to limit
        
        if policy.eligibility.min_vehicle_age is not None:
            if vehicle_age < policy.eligibility.min_vehicle_age:
                return 0.0  # Complete mismatch
        
        # Driver age checks
        if policy.eligibility.max_driver_age is not None:
            if customer.driver.age > policy.eligibility.max_driver_age:
                return 0.0  # Complete mismatch
            elif customer.driver.age >= policy.eligibility.max_driver_age - 2:
                score -= 15.0  # Close to limit
        
        if policy.eligibility.min_driver_age is not None:
            if customer.driver.age < policy.eligibility.min_driver_age:
                return 0.0  # Complete mismatch
        
        # License experience checks
        if policy.eligibility.min_license_years is not None:
            if customer.driver.license_years < policy.eligibility.min_license_years:
                return 0.0  # Complete mismatch
            elif customer.driver.license_years == policy.eligibility.min_license_years:
                score -= 10.0  # Just meets requirement
        
        # Vehicle type restrictions
        if policy.eligibility.excluded_vehicle_types:
            customer_vehicle_type = customer.vehicle.vehicle_type.lower()
            for excluded_type in policy.eligibility.excluded_vehicle_types:
                if excluded_type.lower() in customer_vehicle_type:
                    return 0.0  # Complete mismatch
        
        # Geographic restrictions
        if policy.eligibility.geographic_restrictions:
            customer_state = customer.state.lower()
            for restriction in policy.eligibility.geographic_restrictions:
                if restriction.lower() in customer_state:
                    score -= 30.0
        
        return max(score, 0.0)
    
    def _get_coverage_details(self, policy: PolicyRecord, customer: CustomerInput) -> Dict[str, Any]:
        """Get detailed coverage scoring breakdown"""
        details = {
            "coverage_type": policy.coverage_type,
            "included_benefits": []
        }
        
        # List included benefits
        coverage_fields = [
            'flood', 'theft', 'riot_strike', 'windscreen', 'personal_accident',
            'accessories', 'natural_disaster', 'ehailing_coverage', 
            'passenger_liability', 'legal_liability'
        ]
        
        for field in coverage_fields:
            if getattr(policy.included_cover, field, False):
                details["included_benefits"].append(field.replace('_', ' ').title())
        
        details["benefit_count"] = len(details["included_benefits"])
        
        return details
    
    def _get_service_details(self, policy: PolicyRecord, customer: CustomerInput) -> Dict[str, Any]:
        """Get detailed service scoring breakdown"""
        details = {
            "digital_features": [],
            "roadside_assistance": policy.services.roadside_assist_24_7,
            "workshop_network": policy.services.panel_workshop_count or 0
        }
        
        if policy.services.digital_claims:
            details["digital_features"].append("Digital Claims")
        
        if policy.services.mobile_app:
            details["digital_features"].append("Mobile App")
        
        if policy.services.online_portal:
            details["digital_features"].append("Online Portal")
        
        details["digital_score"] = len(details["digital_features"]) * 10
        
        return details
    
    def _get_pricing_details(self, policy: PolicyRecord, customer: CustomerInput) -> Dict[str, Any]:
        """Get detailed pricing scoring breakdown"""
        details = {
            "available_rebates": len(policy.pricing_notes.rebates),
            "cashback_offers": len(policy.pricing_notes.cashback),
            "bundle_discounts": len(policy.pricing_notes.bundling_discounts),
            "loyalty_benefits": len(policy.pricing_notes.loyalty_benefits),
            "promotional_offers": len(policy.pricing_notes.promotional_offers)
        }
        
        details["total_incentives"] = sum(details.values())
        
        return details

# Global instance
policy_scorer = PolicyScorer()
