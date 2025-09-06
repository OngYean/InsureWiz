"""
Liberty Insurance / AmGeneral scraper stubs
"""

from typing import List
from .base import BaseScraper
from ..models.policy import PolicyRecord

class LibertyScraper(BaseScraper):
    """Scraper for Liberty Insurance"""
    
    def __init__(self):
        super().__init__("Liberty Insurance")
    
    def get_search_terms(self) -> List[str]:
        return [
            "Liberty Insurance Malaysia motor",
            "Liberty car insurance Malaysia",
            "site:libertyinsurance.com.my motor"
        ]
    
    def parse_content(self, content: str, url: str) -> List[PolicyRecord]:
        """Stub implementation for Liberty parsing"""
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

class AmGeneralScraper(BaseScraper):
    """Scraper for AmGeneral"""
    
    def __init__(self):
        super().__init__("AmGeneral")
    
    def get_search_terms(self) -> List[str]:
        return [
            "AmGeneral motor insurance Malaysia",
            "AmGeneral car insurance",
            "site:amgeneral.com motor insurance"
        ]
    
    def parse_content(self, content: str, url: str) -> List[PolicyRecord]:
        """Stub implementation for AmGeneral parsing"""
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
scraper_registry.register("Liberty Insurance", LibertyScraper())
scraper_registry.register("AmGeneral", AmGeneralScraper())
