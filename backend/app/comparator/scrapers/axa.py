"""
AXA Affin General / Generali Malaysia scraper
Stub implementation - to be expanded
"""

from typing import List
from .base import BaseScraper
from ..models.policy import PolicyRecord

class AXAScraper(BaseScraper):
    """Scraper for AXA Affin General"""
    
    def __init__(self):
        super().__init__("AXA Affin General")
    
    def get_search_terms(self) -> List[str]:
        return [
            "AXA Affin motor insurance Malaysia",
            "AXA car insurance Malaysia", 
            "site:axa.com.my motor insurance"
        ]
    
    def parse_content(self, content: str, url: str) -> List[PolicyRecord]:
        """Stub implementation for AXA parsing"""
        policies = []
        
        if 'motor' in content.lower() or 'car insurance' in content.lower():
            policy = self.create_base_policy("Motor Insurance", url)
            policy.coverage_type = self.extract_coverage_type(content)
            policy.eligibility = self.extract_eligibility(content)
            policy.included_cover = self.extract_included_cover(content)
            policy.services = self.extract_services(content)
            policy.pricing_notes = self.extract_pricing_notes(content)
            
            if self.validate_policy(policy):
                policies.append(policy)
        
        self.log_extraction_stats(policies, url)
        return policies

class GeneraliScraper(BaseScraper):
    """Scraper for Generali Malaysia"""
    
    def __init__(self):
        super().__init__("Generali Malaysia")
    
    def get_search_terms(self) -> List[str]:
        return [
            "Generali Malaysia motor insurance",
            "Generali car insurance Malaysia",
            "site:generali.com.my motor insurance"
        ]
    
    def parse_content(self, content: str, url: str) -> List[PolicyRecord]:
        """Stub implementation for Generali parsing"""
        policies = []
        
        if 'motor' in content.lower() or 'car insurance' in content.lower():
            policy = self.create_base_policy("Motor Insurance", url)
            policy.coverage_type = self.extract_coverage_type(content)
            policy.eligibility = self.extract_eligibility(content)
            policy.included_cover = self.extract_included_cover(content)
            policy.services = self.extract_services(content)
            policy.pricing_notes = self.extract_pricing_notes(content)
            
            if self.validate_policy(policy):
                policies.append(policy)
        
        self.log_extraction_stats(policies, url)
        return policies

# Register the scrapers
from .base import scraper_registry
scraper_registry.register("AXA Affin General", AXAScraper())
scraper_registry.register("Generali Malaysia", GeneraliScraper())
