"""
LangChain chains for analyzing and comparing insurance policies
"""

from typing import List, Dict, Any, Optional
import logging
from langchain.prompts import PromptTemplate
from langchain.schema import BaseOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import LLMChain
import json

from ..models.policy import PolicyRecord
from ..models.customer import CustomerInput
from ..models.comparison import PolicyRecommendation, ComparisonResult
from app.config import settings

logger = logging.getLogger(__name__)

class PolicyAnalysisParser(BaseOutputParser):
    """Parser for policy analysis output"""
    
    def parse(self, text: str) -> Dict[str, Any]:
        """Parse the LLM analysis output"""
        try:
            # Extract JSON from response
            start_idx = text.find('{')
            end_idx = text.rfind('}') + 1
            
            if start_idx >= 0 and end_idx > start_idx:
                json_str = text[start_idx:end_idx]
                return json.loads(json_str)
            else:
                # If no JSON, try to parse structured text
                return self._parse_structured_text(text)
        except json.JSONDecodeError:
            return self._parse_structured_text(text)
    
    def _parse_structured_text(self, text: str) -> Dict[str, Any]:
        """Parse structured text format"""
        result = {
            "strengths": [],
            "weaknesses": [],
            "best_for": [],
            "key_features": [],
            "coverage_analysis": "",
            "service_analysis": "",
            "value_analysis": ""
        }
        
        lines = text.split('\n')
        current_section = None
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            if 'strengths:' in line.lower():
                current_section = 'strengths'
            elif 'weaknesses:' in line.lower():
                current_section = 'weaknesses'
            elif 'best for:' in line.lower():
                current_section = 'best_for'
            elif 'key features:' in line.lower():
                current_section = 'key_features'
            elif 'coverage analysis:' in line.lower():
                current_section = 'coverage_analysis'
            elif 'service analysis:' in line.lower():
                current_section = 'service_analysis'
            elif 'value analysis:' in line.lower():
                current_section = 'value_analysis'
            elif line.startswith('- ') and current_section in ['strengths', 'weaknesses', 'best_for', 'key_features']:
                result[current_section].append(line[2:])
            elif current_section in ['coverage_analysis', 'service_analysis', 'value_analysis']:
                if result[current_section]:
                    result[current_section] += " " + line
                else:
                    result[current_section] = line
        
        return result
    
    @property
    def _type(self) -> str:
        return "policy_analysis_parser"

class PolicyAnalysisChain:
    """LangChain chain for analyzing individual policies"""
    
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(
            model=settings.ai_model,
            google_api_key=settings.google_api_key,
            temperature=0.3  # Slightly higher for analysis creativity
        )
        
        self.parser = PolicyAnalysisParser()
        self.chain = self._create_chain()
    
    def _create_chain(self) -> LLMChain:
        """Create the analysis chain"""
        
        template = """
You are a Malaysian motor insurance expert. Analyze the following policy against the customer's needs and provide detailed insights.

Policy Details:
{policy_summary}

Customer Profile:
{customer_profile}

Provide your analysis in the following JSON format:

{{
    "strengths": ["list of policy strengths"],
    "weaknesses": ["list of policy limitations"],
    "best_for": ["scenarios where this policy excels"],
    "key_features": ["unique or standout features"],
    "coverage_analysis": "detailed coverage assessment",
    "service_analysis": "service quality evaluation", 
    "value_analysis": "value for money assessment"
}}

Analysis Guidelines:
- Consider Malaysian insurance market context
- Focus on coverage breadth, service quality, and value
- Highlight unique selling points
- Identify potential gaps or limitations
- Consider customer's specific needs and preferences
- Be objective and balanced in assessment

Return only valid JSON without additional text.
"""
        
        prompt = PromptTemplate(
            input_variables=["policy_summary", "customer_profile"],
            template=template
        )
        
        return LLMChain(
            llm=self.llm,
            prompt=prompt,
            output_parser=self.parser
        )
    
    def analyze_policy(self, policy: PolicyRecord, customer: CustomerInput) -> Dict[str, Any]:
        """Analyze a single policy against customer needs"""
        try:
            # Create policy summary
            policy_summary = self._create_policy_summary(policy)
            
            # Create customer profile
            customer_profile = self._create_customer_profile(customer)
            
            result = self.chain.run(
                policy_summary=policy_summary,
                customer_profile=customer_profile
            )
            
            logger.info(f"Analyzed policy: {policy.insurer} - {policy.product_name}")
            return result if isinstance(result, dict) else {}
            
        except Exception as e:
            logger.error(f"Error analyzing policy: {e}")
            return {}
    
    def _create_policy_summary(self, policy: PolicyRecord) -> str:
        """Create a concise policy summary for analysis"""
        summary_parts = [
            f"Insurer: {policy.insurer}",
            f"Product: {policy.product_name}",
            f"Type: {'Takaful' if policy.is_takaful else 'Conventional'}",
            f"Coverage: {policy.coverage_type}",
        ]
        
        if policy.valuation_method:
            summary_parts.append(f"Valuation: {policy.valuation_method}")
        
        # Include key coverage points
        coverage_points = []
        if policy.included_cover.flood:
            coverage_points.append("Flood")
        if policy.included_cover.theft:
            coverage_points.append("Theft") 
        if policy.included_cover.windscreen:
            coverage_points.append("Windscreen")
        if policy.included_cover.personal_accident:
            coverage_points.append("Personal Accident")
        
        if coverage_points:
            summary_parts.append(f"Included: {', '.join(coverage_points)}")
        
        # Include key services
        service_points = []
        if policy.services.roadside_assist_24_7:
            service_points.append("24/7 Roadside")
        if policy.services.digital_claims:
            service_points.append("Digital Claims")
        if policy.services.mobile_app:
            service_points.append("Mobile App")
        
        if service_points:
            summary_parts.append(f"Services: {', '.join(service_points)}")
        
        return "\n".join(summary_parts)
    
    def _create_customer_profile(self, customer: CustomerInput) -> str:
        """Create customer profile for analysis"""
        profile_parts = [
            f"Driver Age: {customer.driver.age}",
            f"License Years: {customer.driver.license_years}",
            f"Vehicle: {customer.vehicle.year} {customer.vehicle.make} {customer.vehicle.model}",
            f"Vehicle Type: {customer.vehicle.vehicle_type}",
            f"State: {customer.state}",
            f"Usage: {customer.vehicle.usage_type}",
        ]
        
        if customer.preferences.takaful_preference:
            profile_parts.append("Prefers Takaful products")
        
        profile_parts.append(f"Coverage Priority: {customer.preferences.coverage_priority}")
        
        if customer.preferences.important_features:
            profile_parts.append(f"Important Features: {', '.join(customer.preferences.important_features)}")
        
        if customer.preferences.service_priorities:
            profile_parts.append(f"Service Priorities: {', '.join(customer.preferences.service_priorities)}")
        
        return "\n".join(profile_parts)

class PolicyComparisonChain:
    """LangChain chain for comparing multiple policies"""
    
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(
            model=settings.ai_model,
            google_api_key=settings.google_api_key,
            temperature=0.4
        )
        
        self.analysis_chain = PolicyAnalysisChain()
    
    def compare_policies(self, policies: List[PolicyRecord], customer: CustomerInput) -> Dict[str, Any]:
        """Compare multiple policies and provide insights"""
        try:
            # Create comparison summary
            comparison_summary = self._create_comparison_summary(policies, customer)
            
            template = """
You are a Malaysian insurance expert comparing motor insurance policies for a customer.

{comparison_summary}

Provide market insights and general recommendations in JSON format:

{{
    "market_insights": ["key insights about the insurance market"],
    "general_recommendations": ["general advice for the customer"],
    "top_considerations": ["most important factors to consider"],
    "next_steps": ["recommended actions for the customer"]
}}

Focus on:
- Malaysian market dynamics
- Regulatory considerations (BNM compliance)
- Value proposition comparison
- Risk assessment
- Customer-specific advice

Return only valid JSON.
"""
            
            prompt = PromptTemplate(
                input_variables=["comparison_summary"],
                template=template
            )
            
            chain = LLMChain(llm=self.llm, prompt=prompt)
            
            result = chain.run(comparison_summary=comparison_summary)
            
            if isinstance(result, str):
                try:
                    result = json.loads(result)
                except json.JSONDecodeError:
                    result = {}
            
            return result if isinstance(result, dict) else {}
            
        except Exception as e:
            logger.error(f"Error in policy comparison: {e}")
            return {}
    
    def _create_comparison_summary(self, policies: List[PolicyRecord], customer: CustomerInput) -> str:
        """Create comparison summary for analysis"""
        summary_parts = [
            f"Customer Profile:",
            f"- Age: {customer.driver.age}, License: {customer.driver.license_years} years",
            f"- Vehicle: {customer.vehicle.year} {customer.vehicle.make} {customer.vehicle.model}",
            f"- State: {customer.state}",
            f"- Takaful Preference: {'Yes' if customer.preferences.takaful_preference else 'No'}",
            f"- Coverage Priority: {customer.preferences.coverage_priority}",
            "",
            f"Policies to Compare ({len(policies)} total):"
        ]
        
        for i, policy in enumerate(policies, 1):
            summary_parts.extend([
                f"{i}. {policy.insurer} - {policy.product_name}",
                f"   Type: {'Takaful' if policy.is_takaful else 'Conventional'} | Coverage: {policy.coverage_type}",
                f"   Key Features: {self._get_key_features(policy)}",
                ""
            ])
        
        return "\n".join(summary_parts)
    
    def _get_key_features(self, policy: PolicyRecord) -> str:
        """Get key features summary for a policy"""
        features = []
        
        if policy.included_cover.flood:
            features.append("Flood")
        if policy.included_cover.windscreen:
            features.append("Windscreen")
        if policy.services.roadside_assist_24_7:
            features.append("24/7 Roadside")
        if policy.services.digital_claims:
            features.append("Digital Claims")
        
        return ", ".join(features) if features else "Standard coverage"

# Global instances
analysis_chain = PolicyAnalysisChain()
comparison_chain = PolicyComparisonChain()
