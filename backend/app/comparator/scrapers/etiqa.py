"""
Etiqa insurance scraper
Handles parsing of Private Car Insurance and Takaful products
"""

import re
from typing import List, Dict, Any
from .base import BaseScraper
from ..models.policy import PolicyRecord, CoverageType, ValuationMethod

class EtiqaScraper(BaseScraper):
    """Scraper for Etiqa motor insurance products"""
    
    def __init__(self):
        super().__init__("Etiqa")
    
    def get_search_terms(self) -> List[str]:
        """Search terms for discovering Etiqa URLs"""
        return [
            "Etiqa motor insurance Malaysia",
            "Etiqa private car insurance",
            "Etiqa takaful motor",
            "Etiqa comprehensive motor",
            "site:etiqa.com.my motor insurance",
            "site:etiqa.com.my car insurance",
            "Etiqa vehicle insurance"
        ]
    
    def parse_content(self, content: str, url: str) -> List[PolicyRecord]:
        """Parse Etiqa policy content"""
        policies = []
        
        # Check for Takaful vs Conventional
        is_takaful = self._is_takaful_page(content)
        
        # Detect product types
        if self._is_private_car_page(content):
            policy = self._parse_private_car(content, url, is_takaful)
            if policy and self.validate_policy(policy):
                policies.append(policy)
        
        if self._is_comprehensive_page(content):
            policy = self._parse_comprehensive(content, url, is_takaful)
            if policy and self.validate_policy(policy):
                policies.append(policy)
        
        # Try general parsing if no specific products found
        if not policies:
            general_policies = self._parse_general_motor(content, url, is_takaful)
            policies.extend(general_policies)
        
        self.log_extraction_stats(policies, url)
        return policies
    
    def _is_takaful_page(self, content: str) -> bool:
        """Check if content is about Takaful products"""
        indicators = ['takaful', 'shariah', 'islamic', 'halal']
        return any(indicator in content.lower() for indicator in indicators)
    
    def _is_private_car_page(self, content: str) -> bool:
        """Check if content is about Private Car Insurance"""
        indicators = ['private car', 'personal car', 'individual car']
        return any(indicator in content.lower() for indicator in indicators)
    
    def _is_comprehensive_page(self, content: str) -> bool:
        """Check if content is about Comprehensive coverage"""
        indicators = ['comprehensive', 'full coverage', 'complete protection']
        return any(indicator in content.lower() for indicator in indicators)
    
    def _parse_private_car(self, content: str, url: str, is_takaful: bool) -> PolicyRecord:
        """Parse Private Car Insurance content"""
        product_name = "Private Car Takaful" if is_takaful else "Private Car Insurance"
        policy = self.create_base_policy(product_name, url, is_takaful)
        
        # Determine coverage type
        policy.coverage_type = self.extract_coverage_type(content)
        
        # Extract valuation method
        policy.valuation_method = self.extract_valuation_method(content)
        if not policy.valuation_method:
            policy.valuation_method = ValuationMethod.MARKET_VALUE  # Etiqa default
        
        # Extract eligibility
        policy.eligibility = self.extract_eligibility(content)
        
        # Extract coverage
        policy.included_cover = self.extract_included_cover(content)
        
        # Etiqa private car typically includes
        policy.included_cover.theft = True
        policy.included_cover.windscreen = True
        
        # Extract add-ons
        policy.addons = self._extract_etiqa_addons(content)
        
        # Extract services
        policy.services = self.extract_services(content)
        
        # Etiqa services
        policy.services.digital_claims = True
        if 'e-claim' in content.lower():
            policy.services.digital_claims = True
        
        # Extract pricing notes
        policy.pricing_notes = self.extract_pricing_notes(content)
        
        # Etiqa-specific pricing features
        if 'renewal discount' in content.lower():
            policy.pricing_notes.loyalty_benefits.append("Renewal discount available")
        
        return policy
    
    def _parse_comprehensive(self, content: str, url: str, is_takaful: bool) -> PolicyRecord:
        """Parse Comprehensive coverage content"""
        product_name = "Comprehensive Takaful" if is_takaful else "Comprehensive Motor"
        policy = self.create_base_policy(product_name, url, is_takaful)
        
        policy.coverage_type = CoverageType.COMPREHENSIVE
        
        # Extract valuation method
        policy.valuation_method = self.extract_valuation_method(content)
        
        # Extract eligibility
        policy.eligibility = self.extract_eligibility(content)
        
        # Comprehensive coverage includes more benefits
        policy.included_cover = self.extract_included_cover(content)
        policy.included_cover.flood = True
        policy.included_cover.theft = True
        policy.included_cover.riot_strike = True
        policy.included_cover.windscreen = True
        policy.included_cover.natural_disaster = True
        
        # Extract add-ons
        policy.addons = self._extract_etiqa_addons(content)
        
        # Extract services
        policy.services = self.extract_services(content)
        policy.services.roadside_assist_24_7 = True
        
        # Extract pricing notes
        policy.pricing_notes = self.extract_pricing_notes(content)
        
        return policy
    
    def _parse_general_motor(self, content: str, url: str, is_takaful: bool) -> List[PolicyRecord]:
        """Parse general motor insurance content"""
        policies = []
        
        if 'motor' in content.lower() or 'vehicle' in content.lower():
            product_name = "Motor Takaful" if is_takaful else "Motor Insurance"
            policy = self.create_base_policy(product_name, url, is_takaful)
            
            # Extract basic information
            policy.coverage_type = self.extract_coverage_type(content)
            policy.eligibility = self.extract_eligibility(content)
            policy.included_cover = self.extract_included_cover(content)
            policy.services = self.extract_services(content)
            policy.pricing_notes = self.extract_pricing_notes(content)
            
            if self.validate_policy(policy):
                policies.append(policy)
        
        return policies
    
    def _extract_etiqa_addons(self, content: str) -> Any:
        """Extract Etiqa-specific add-ons"""
        from ..models.policy import AddOns
        
        addons = AddOns()
        content_lower = content.lower()
        
        # NCD Protection
        if any(term in content_lower for term in ['ncd protection', 'no claim bonus protection']):
            addons.ncd_protection = {
                "available": True,
                "description": "No Claim Discount Protection"
            }
        
        # Key Care/Replacement
        if any(term in content_lower for term in ['key care', 'key replacement', 'smart key']):
            addons.key_replacement = {
                "available": True,
                "description": "Key Care coverage"
            }
        
        # Courtesy Car
        if any(term in content_lower for term in ['courtesy car', 'replacement car']):
            addons.courtesy_car = {
                "available": True,
                "description": "Courtesy car service"
            }
        
        # Enhanced Towing
        if any(term in content_lower for term in ['enhanced towing', 'extended towing']):
            addons.towing_service = {
                "available": True,
                "description": "Enhanced towing service"
            }
        
        # Loss of Use
        if any(term in content_lower for term in ['loss of use', 'daily allowance']):
            addons.loss_of_use = {
                "available": True,
                "description": "Loss of use compensation"
            }
        
        # Medical Benefits
        if any(term in content_lower for term in ['medical benefit', 'hospital benefit']):
            addons.hospital_cash = {
                "available": True,
                "description": "Medical/Hospital benefits"
            }
        
        # Strike, Riot & Civil Commotion (SRCC) Extension
        if any(term in content_lower for term in ['srcc', 'strike riot', 'civil commotion']):
            # This might be standard coverage rather than addon
            pass
        
        # Legal Liability to Passengers
        if any(term in content_lower for term in ['legal liability', 'passenger liability']):
            # Usually standard in comprehensive
            pass
        
        return addons

# Register the scraper
from .base import scraper_registry
scraper_registry.register("Etiqa", EtiqaScraper())
