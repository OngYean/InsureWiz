"""
Berjaya Sompo scraper stub
"""

from typing import List
from .base import BaseScraper
from ..models.policy import PolicyRecord

class SompoScraper(BaseScraper):
    """Scraper for Berjaya Sompo"""
    
    def __init__(self):
        super().__init__("Berjaya Sompo")
    
    def get_search_terms(self) -> List[str]:
        return [
            "Berjaya Sompo motor insurance",
            "Sompo car insurance Malaysia",
            "site:berjayasompo.com.my motor",
            "Berjaya Sompo comprehensive motor"
        ]
    
    def parse_content(self, content: str, url: str) -> List[PolicyRecord]:
        """Stub implementation for Berjaya Sompo parsing"""
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
scraper_registry.register("Berjaya Sompo", SompoScraper())
