"""
LangChain chains for extracting structured data from crawled insurance content
"""

from typing import List, Dict, Any, Optional
import logging
from langchain.prompts import PromptTemplate
from langchain.schema import BaseOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import LLMChain
import json

from ..models.policy import PolicyRecord, CoverageType, ValuationMethod
from app.config import settings

logger = logging.getLogger(__name__)

class PolicyExtractionParser(BaseOutputParser):
    """Parser for policy extraction output"""
    
    def parse(self, text: str) -> Dict[str, Any]:
        """Parse the LLM output into structured policy data"""
        try:
            # Try to extract JSON from the response
            start_idx = text.find('{')
            end_idx = text.rfind('}') + 1
            
            if start_idx >= 0 and end_idx > start_idx:
                json_str = text[start_idx:end_idx]
                return json.loads(json_str)
            else:
                logger.warning("No valid JSON found in LLM response")
                return {}
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse LLM output as JSON: {e}")
            return {}
    
    @property
    def _type(self) -> str:
        return "policy_extraction_parser"

class PolicyExtractionChain:
    """LangChain chain for extracting policy information from web content"""
    
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(
            model=settings.ai_model,
            google_api_key=settings.google_api_key,
            temperature=0.1  # Low temperature for factual extraction
        )
        
        self.parser = PolicyExtractionParser()
        self.chain = self._create_chain()
    
    def _create_chain(self) -> LLMChain:
        """Create the extraction chain"""
        
        template = """
You are an expert insurance policy analyst. Extract structured information from the following Malaysian motor insurance content.

Content: {content}
URL: {url}
Insurer: {insurer}

Extract the following information and return it as valid JSON:

{{
    "product_name": "Name of the insurance product",
    "is_takaful": true/false,
    "coverage_type": "Comprehensive" | "Third Party, Fire & Theft" | "Third Party",
    "valuation_method": "Agreed Value" | "Market Value" | null,
    "eligibility": {{
        "min_vehicle_age": number or null,
        "max_vehicle_age": number or null,
        "min_driver_age": number or null,
        "max_driver_age": number or null,
        "min_license_years": number or null,
        "excluded_vehicle_types": ["list of excluded types"],
        "geographic_restrictions": ["list of geographic restrictions"]
    }},
    "included_cover": {{
        "flood": true/false,
        "theft": true/false,
        "riot_strike": true/false,
        "windscreen": true/false,
        "personal_accident": true/false,
        "accessories": true/false,
        "natural_disaster": true/false,
        "ehailing_coverage": true/false,
        "passenger_liability": true/false,
        "legal_liability": true/false
    }},
    "addons": {{
        "ncd_protection": {{"available": true/false, "description": "text"}},
        "key_replacement": {{"available": true/false, "description": "text"}},
        "courtesy_car": {{"available": true/false, "description": "text"}},
        "towing_service": {{"available": true/false, "description": "text"}},
        "loss_of_use": {{"available": true/false, "description": "text"}},
        "hospital_cash": {{"available": true/false, "description": "text"}},
        "betterment_waiver": {{"available": true/false, "description": "text"}},
        "unnamed_driver": {{"available": true/false, "description": "text"}}
    }},
    "services": {{
        "roadside_assist_24_7": true/false,
        "roadside_assist_sla": "response time or null",
        "towing_limit": "limit description or null", 
        "claim_fast_track": true/false,
        "fast_track_threshold": "threshold amount or null",
        "panel_workshop_count": number or null,
        "digital_claims": true/false,
        "mobile_app": true/false,
        "online_portal": true/false
    }},
    "pricing_notes": {{
        "rebates": ["list of available rebates"],
        "cashback": ["list of cashback offers"],
        "bundling_discounts": ["list of bundle discounts"],
        "loyalty_benefits": ["list of loyalty benefits"],
        "promotional_offers": ["list of current promotions"]
    }},
    "exclusions": ["list of policy exclusions"]
}}

Rules:
- Only extract information that is explicitly mentioned in the content
- Use null for missing information
- Be conservative - if uncertain, use false/null
- Focus on factual information, not marketing language
- Extract numeric values where possible (ages, amounts, counts)
- Identify Takaful products by keywords: takaful, shariah, islamic, halal

Return only valid JSON without additional text or explanation.
"""
        
        prompt = PromptTemplate(
            input_variables=["content", "url", "insurer"],
            template=template
        )
        
        return LLMChain(
            llm=self.llm,
            prompt=prompt,
            output_parser=self.parser
        )
    
    def extract_policy_data(self, content: str, url: str, insurer: str) -> Optional[Dict[str, Any]]:
        """Extract policy data from content"""
        try:
            result = self.chain.run(
                content=content[:8000],  # Limit content length
                url=url,
                insurer=insurer
            )
            
            if isinstance(result, dict) and result:
                logger.info(f"Successfully extracted policy data for {insurer}")
                return result
            else:
                logger.warning(f"Empty or invalid extraction result for {insurer}")
                return None
                
        except Exception as e:
            logger.error(f"Error extracting policy data: {e}")
            return None
    
    def create_policy_record(self, extracted_data: Dict[str, Any], url: str, insurer: str) -> Optional[PolicyRecord]:
        """Create a PolicyRecord from extracted data"""
        try:
            # Map extracted data to PolicyRecord
            policy_data = {
                "insurer": insurer,
                "product_name": extracted_data.get("product_name", "Motor Insurance"),
                "is_takaful": extracted_data.get("is_takaful", False),
                "coverage_type": extracted_data.get("coverage_type", "Comprehensive"),
                "valuation_method": extracted_data.get("valuation_method"),
                "eligibility": extracted_data.get("eligibility", {}),
                "included_cover": extracted_data.get("included_cover", {}),
                "addons": extracted_data.get("addons", {}),
                "services": extracted_data.get("services", {}),
                "pricing_notes": extracted_data.get("pricing_notes", {}),
                "exclusions": extracted_data.get("exclusions", []),
                "source_urls": [url]
            }
            
            # Create PolicyRecord instance
            policy = PolicyRecord(**policy_data)
            
            logger.info(f"Created policy record: {policy.product_name}")
            return policy
            
        except Exception as e:
            logger.error(f"Error creating policy record: {e}")
            return None

class MultiPolicyExtractionChain:
    """Chain for extracting multiple policies from content"""
    
    def __init__(self):
        self.extraction_chain = PolicyExtractionChain()
    
    def extract_policies(self, content: str, url: str, insurer: str) -> List[PolicyRecord]:
        """Extract multiple policies from content"""
        policies = []
        
        # First, try to identify if there are multiple products mentioned
        product_sections = self._split_content_by_products(content)
        
        if len(product_sections) > 1:
            # Extract each product separately
            for section in product_sections:
                extracted_data = self.extraction_chain.extract_policy_data(section, url, insurer)
                if extracted_data:
                    policy = self.extraction_chain.create_policy_record(extracted_data, url, insurer)
                    if policy:
                        policies.append(policy)
        else:
            # Extract as single policy
            extracted_data = self.extraction_chain.extract_policy_data(content, url, insurer)
            if extracted_data:
                policy = self.extraction_chain.create_policy_record(extracted_data, url, insurer)
                if policy:
                    policies.append(policy)
        
        return policies
    
    def _split_content_by_products(self, content: str) -> List[str]:
        """Split content into sections by product mentions"""
        # Simple heuristic - look for product names
        product_keywords = [
            'comprehensive', 'third party', 'z-driver', 'takaful',
            'motor insurance', 'car insurance', 'vehicle insurance'
        ]
        
        # For now, return content as single section
        # TODO: Implement more sophisticated content splitting
        return [content]

# Global instances
extraction_chain = PolicyExtractionChain()
multi_extraction_chain = MultiPolicyExtractionChain()
