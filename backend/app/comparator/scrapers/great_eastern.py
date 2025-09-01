"""
Great Eastern General scraper stub
"""

from typing import List
from .base import BaseScraper
from ..models.policy import PolicyRecord

class GreatEasternScraper(BaseScraper):
    """Scraper for Great Eastern General"""
    
    def __init__(self):
        super().__init__("Great Eastern General")
    
    def get_search_terms(self) -> List[str]:
        return [
            "Great Eastern motor insurance Malaysia",
            "Great Eastern car insurance",
            "site:greateastern.com.my motor insurance",
            "Great Eastern general insurance motor"
        ]
    
    def parse_content(self, content: str, url: str) -> List[PolicyRecord]:
        """Stub implementation for Great Eastern parsing"""
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

# Register the scraper
from .base import scraper_registry
scraper_registry.register("Great Eastern General", GreatEasternScraper())
