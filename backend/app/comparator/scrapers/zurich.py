"""
Zurich Malaysia insurance scraper
Handles parsing of Z-Driver and Motor Comprehensive policies
"""

import re
from typing import List, Dict, Any
from .base import BaseScraper
from ..models.policy import PolicyRecord, CoverageType, ValuationMethod

class ZurichScraper(BaseScraper):
    """Scraper for Zurich Malaysia motor insurance products"""
    
    def __init__(self):
        super().__init__("Zurich Malaysia")
    
    def get_search_terms(self) -> List[str]:
        """Search terms for discovering Zurich URLs"""
        return [
            "Zurich Malaysia motor insurance",
            "Zurich Z-Driver",
            "Zurich Motor Comprehensive",
            "Zurich car insurance Malaysia",
            "site:zurich.com.my motor insurance",
            "site:zurich.com.my Z-Driver"
        ]
    
    def parse_content(self, content: str, url: str) -> List[PolicyRecord]:
        """Parse Zurich policy content"""
        policies = []
        
        # Detect if this is Z-Driver or Motor Comprehensive
        if self._is_z_driver_page(content):
            policy = self._parse_z_driver(content, url)
            if policy and self.validate_policy(policy):
                policies.append(policy)
        
        if self._is_motor_comprehensive_page(content):
            policy = self._parse_motor_comprehensive(content, url)
            if policy and self.validate_policy(policy):
                policies.append(policy)
        
        # If we can't identify specific products, try general parsing
        if not policies:
            general_policies = self._parse_general_motor(content, url)
            policies.extend(general_policies)
        
        self.log_extraction_stats(policies, url)
        return policies
    
    def _is_z_driver_page(self, content: str) -> bool:
        """Check if content is about Z-Driver product"""
        indicators = ['z-driver', 'z driver', 'young driver', 'graduate']
        return any(indicator in content.lower() for indicator in indicators)
    
    def _is_motor_comprehensive_page(self, content: str) -> bool:
        """Check if content is about Motor Comprehensive product"""
        indicators = ['motor comprehensive', 'comprehensive motor', 'full coverage']
        return any(indicator in content.lower() for indicator in indicators)
    
    def _parse_z_driver(self, content: str, url: str) -> PolicyRecord:
        """Parse Z-Driver specific content"""
        policy = self.create_base_policy("Z-Driver", url)
        policy.coverage_type = CoverageType.COMPREHENSIVE
        
        # Z-Driver specific features
        content_lower = content.lower()
        
        # Young driver focus
        if 'young driver' in content_lower or 'graduate' in content_lower:
            policy.eligibility.min_driver_age = 18
            policy.eligibility.max_driver_age = 35
        
        # Extract specific Z-Driver features
        policy.included_cover = self.extract_included_cover(content)
        
        # Z-Driver typically includes
        policy.included_cover.windscreen = True
        policy.included_cover.personal_accident = True
        
        # Extract add-ons
        policy.addons = self._extract_zurich_addons(content)
        
        # Extract services
        policy.services = self.extract_services(content)
        policy.services.mobile_app = True  # Zurich has mobile app
        
        # Extract pricing notes
        policy.pricing_notes = self.extract_pricing_notes(content)
        
        # Check for graduate discount
        if 'graduate' in content_lower:
            policy.pricing_notes.rebates.append("Graduate discount available")
        
        return policy
    
    def _parse_motor_comprehensive(self, content: str, url: str) -> PolicyRecord:
        """Parse Motor Comprehensive specific content"""
        policy = self.create_base_policy("Motor Comprehensive", url)
        policy.coverage_type = CoverageType.COMPREHENSIVE
        
        # Standard comprehensive coverage
        policy.valuation_method = self.extract_valuation_method(content)
        
        # Extract coverage details
        policy.included_cover = self.extract_included_cover(content)
        
        # Comprehensive typically includes more coverage
        policy.included_cover.flood = True
        policy.included_cover.theft = True
        policy.included_cover.riot_strike = True
        policy.included_cover.windscreen = True
        
        # Extract add-ons
        policy.addons = self._extract_zurich_addons(content)
        
        # Extract services
        policy.services = self.extract_services(content)
        policy.services.mobile_app = True
        policy.services.roadside_assist_24_7 = True
        
        # Extract pricing notes
        policy.pricing_notes = self.extract_pricing_notes(content)
        
        return policy
    
    def _parse_general_motor(self, content: str, url: str) -> List[PolicyRecord]:
        """Parse general motor insurance content"""
        policies = []
        
        # Look for product mentions
        if 'motor' in content.lower() or 'car insurance' in content.lower():
            policy = self.create_base_policy("Motor Insurance", url)
            policy.coverage_type = self.extract_coverage_type(content)
            
            # Extract basic information
            policy.eligibility = self.extract_eligibility(content)
            policy.included_cover = self.extract_included_cover(content)
            policy.services = self.extract_services(content)
            policy.pricing_notes = self.extract_pricing_notes(content)
            
            if self.validate_policy(policy):
                policies.append(policy)
        
        return policies
    
    def _extract_zurich_addons(self, content: str) -> Any:
        """Extract Zurich-specific add-ons"""
        from ..models.policy import AddOns
        
        addons = AddOns()
        content_lower = content.lower()
        
        # NCD Protection
        if any(term in content_lower for term in ['ncd protection', 'no claim discount protection']):
            addons.ncd_protection = {
                "available": True,
                "description": "NCD Protection available"
            }
        
        # Key Replacement
        if any(term in content_lower for term in ['key replacement', 'key cover', 'lost key']):
            addons.key_replacement = {
                "available": True,
                "description": "Key replacement coverage"
            }
        
        # Courtesy Car
        if any(term in content_lower for term in ['courtesy car', 'replacement vehicle', 'hire car']):
            addons.courtesy_car = {
                "available": True,
                "description": "Courtesy car provision"
            }
        
        # Towing
        if any(term in content_lower for term in ['towing', 'tow truck', 'breakdown']):
            addons.towing_service = {
                "available": True,
                "description": "Towing service included"
            }
        
        # Hospital Cash
        if any(term in content_lower for term in ['hospital cash', 'medical benefit']):
            addons.hospital_cash = {
                "available": True,
                "description": "Hospital cash benefit"
            }
        
        # Betterment Waiver
        if any(term in content_lower for term in ['betterment waiver', 'depreciation waiver']):
            addons.betterment_waiver = {
                "available": True,
                "description": "Betterment charges waiver"
            }
        
        return addons

# Register the scraper
from .base import scraper_registry
scraper_registry.register("Zurich Malaysia", ZurichScraper())
