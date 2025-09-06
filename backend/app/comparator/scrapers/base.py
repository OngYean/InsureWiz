"""
Base scraper class and common utilities for insurance policy extraction
"""

from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any, Union
import re
import logging
from datetime import datetime

from ..models.policy import PolicyRecord, CoverageType, ValuationMethod
from ..models.policy import Eligibility, IncludedCover, AddOns, Services, PricingNotes

logger = logging.getLogger(__name__)

class BaseScraper(ABC):
    """Base class for insurance company scrapers"""
    
    def __init__(self, insurer_name: str):
        self.insurer_name = insurer_name
        self.logger = logging.getLogger(f"{__name__}.{insurer_name}")
    
    @abstractmethod
    def parse_content(self, content: str, url: str) -> List[PolicyRecord]:
        """Parse crawled content and return policy records"""
        pass
    
    @abstractmethod
    def get_search_terms(self) -> List[str]:
        """Get search terms for discovering URLs"""
        pass
    
    def extract_coverage_type(self, text: str) -> CoverageType:
        """Extract coverage type from text"""
        text_lower = text.lower()
        
        if any(term in text_lower for term in ['comprehensive', 'comp', 'full cover']):
            return CoverageType.COMPREHENSIVE
        elif any(term in text_lower for term in ['third party fire theft', 'tpft', 'tp fire theft']):
            return CoverageType.TPFT
        elif any(term in text_lower for term in ['third party', 'tp only', 'basic']):
            return CoverageType.THIRD_PARTY
        
        # Default to comprehensive if unclear
        return CoverageType.COMPREHENSIVE
    
    def extract_valuation_method(self, text: str) -> Optional[ValuationMethod]:
        """Extract valuation method from text"""
        text_lower = text.lower()
        
        if any(term in text_lower for term in ['agreed value', 'agreed sum']):
            return ValuationMethod.AGREED_VALUE
        elif any(term in text_lower for term in ['market value', 'current market', 'depreciated']):
            return ValuationMethod.MARKET_VALUE
        
        return None
    
    def extract_boolean_coverage(self, text: str, keywords: List[str]) -> bool:
        """Check if coverage is mentioned in text"""
        text_lower = text.lower()
        return any(keyword.lower() in text_lower for keyword in keywords)
    
    def extract_age_limit(self, text: str, limit_type: str = "max") -> Optional[int]:
        """Extract age limits from text"""
        patterns = [
            r'(\d+)\s*years?\s*(?:old|age)',
            r'age[d]?\s*(\d+)',
            r'(\d+)\s*year[s]?'
        ]
        
        ages = []
        for pattern in patterns:
            matches = re.findall(pattern, text.lower())
            ages.extend([int(match) for match in matches])
        
        if not ages:
            return None
        
        return max(ages) if limit_type == "max" else min(ages)
    
    def extract_currency_amounts(self, text: str) -> List[float]:
        """Extract currency amounts from text"""
        patterns = [
            r'rm\s*([0-9,]+(?:\.[0-9]{2})?)',
            r'\$\s*([0-9,]+(?:\.[0-9]{2})?)',
            r'(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)\s*(?:ringgit|rm)'
        ]
        
        amounts = []
        for pattern in patterns:
            matches = re.findall(pattern, text.lower())
            for match in matches:
                try:
                    amount = float(match.replace(',', ''))
                    amounts.append(amount)
                except ValueError:
                    continue
        
        return amounts
    
    def extract_eligibility(self, text: str) -> Eligibility:
        """Extract eligibility criteria from text"""
        eligibility = Eligibility()
        
        # Extract vehicle age limits
        if 'vehicle age' in text.lower() or 'car age' in text.lower():
            max_age = self.extract_age_limit(text, "max")
            if max_age:
                eligibility.max_vehicle_age = max_age
        
        # Extract driver age limits
        if 'driver age' in text.lower() or 'minimum age' in text.lower():
            min_age = self.extract_age_limit(text, "min")
            max_age = self.extract_age_limit(text, "max")
            if min_age:
                eligibility.min_driver_age = min_age
            if max_age:
                eligibility.max_driver_age = max_age
        
        # Extract license requirements
        license_patterns = [
            r'(\d+)\s*years?\s*(?:driving\s*)?(?:license|licence)',
            r'(?:license|licence)\s*(?:for\s*)?(\d+)\s*years?'
        ]
        
        for pattern in license_patterns:
            matches = re.findall(pattern, text.lower())
            if matches:
                eligibility.min_license_years = int(matches[0])
                break
        
        return eligibility
    
    def extract_included_cover(self, text: str) -> IncludedCover:
        """Extract included coverage from text"""
        cover = IncludedCover()
        
        # Define coverage keywords
        coverage_mapping = {
            'flood': ['flood', 'flooding', 'water damage'],
            'theft': ['theft', 'stealing', 'stolen'],
            'riot_strike': ['riot', 'strike', 'civil commotion', 'malicious damage'],
            'windscreen': ['windscreen', 'windshield', 'glass'],
            'personal_accident': ['personal accident', 'pa cover', 'driver accident'],
            'accessories': ['accessories', 'additional equipment', 'add-on equipment'],
            'natural_disaster': ['natural disaster', 'earthquake', 'landslide', 'tsunami'],
            'ehailing_coverage': ['e-hailing', 'grab', 'uber', 'commercial use'],
            'passenger_liability': ['passenger liability', 'passenger protection'],
            'legal_liability': ['legal liability', 'third party liability']
        }
        
        text_lower = text.lower()
        for field, keywords in coverage_mapping.items():
            if any(keyword in text_lower for keyword in keywords):
                setattr(cover, field, True)
        
        return cover
    
    def extract_services(self, text: str) -> Services:
        """Extract service offerings from text"""
        services = Services()
        text_lower = text.lower()
        
        # 24/7 roadside assistance
        if any(term in text_lower for term in ['24/7', '24 hours', 'round the clock', 'anytime']):
            if any(term in text_lower for term in ['roadside', 'assistance', 'breakdown']):
                services.roadside_assist_24_7 = True
        
        # Fast track claims
        if any(term in text_lower for term in ['fast track', 'express claim', 'quick claim']):
            services.claim_fast_track = True
        
        # Digital services
        if any(term in text_lower for term in ['digital', 'online', 'mobile app', 'e-claim']):
            services.digital_claims = True
        
        if 'mobile app' in text_lower or 'app' in text_lower:
            services.mobile_app = True
        
        if any(term in text_lower for term in ['online portal', 'web portal', 'customer portal']):
            services.online_portal = True
        
        # Extract workshop count
        workshop_patterns = [
            r'(\d+)\s*(?:panel\s*)?workshops?',
            r'(?:over\s*)?(\d+)\s*authorized\s*workshops?'
        ]
        
        for pattern in workshop_patterns:
            matches = re.findall(pattern, text_lower)
            if matches:
                services.panel_workshop_count = int(matches[0])
                break
        
        return services
    
    def extract_pricing_notes(self, text: str) -> PricingNotes:
        """Extract pricing and promotional information"""
        pricing = PricingNotes()
        text_lower = text.lower()
        
        # Rebates
        if any(term in text_lower for term in ['rebate', 'discount', 'reduction']):
            pricing.rebates.append("Rebates available")
        
        # Cashback
        if 'cashback' in text_lower or 'cash back' in text_lower:
            pricing.cashback.append("Cashback offered")
        
        # Bundling
        if any(term in text_lower for term in ['bundle', 'package', 'combined']):
            pricing.bundling_discounts.append("Bundle discounts available")
        
        # Loyalty
        if any(term in text_lower for term in ['loyalty', 'existing customer', 'renewal']):
            pricing.loyalty_benefits.append("Loyalty benefits available")
        
        return pricing
    
    def create_base_policy(self, product_name: str, url: str, is_takaful: bool = False) -> PolicyRecord:
        """Create a base policy record with common fields"""
        return PolicyRecord(
            insurer=self.insurer_name,
            product_name=product_name,
            is_takaful=is_takaful,
            coverage_type=CoverageType.COMPREHENSIVE,  # Default
            source_urls=[url],
            last_checked=datetime.now()
        )
    
    def validate_policy(self, policy: PolicyRecord) -> bool:
        """Validate that policy has minimum required information"""
        if not policy.insurer or not policy.product_name:
            return False
        
        if not policy.coverage_type:
            return False
        
        return True
    
    def log_extraction_stats(self, policies: List[PolicyRecord], url: str):
        """Log extraction statistics"""
        self.logger.info(f"Extracted {len(policies)} policies from {url}")
        for policy in policies:
            self.logger.debug(f"  - {policy.product_name} ({policy.coverage_type})")


class ScraperRegistry:
    """Registry for managing scrapers"""
    
    def __init__(self):
        self._scrapers: Dict[str, BaseScraper] = {}
    
    def register(self, insurer: str, scraper: BaseScraper):
        """Register a scraper for an insurer"""
        self._scrapers[insurer.lower()] = scraper
        logger.info(f"Registered scraper for {insurer}")
    
    def get_scraper(self, insurer: str) -> Optional[BaseScraper]:
        """Get scraper for an insurer"""
        return self._scrapers.get(insurer.lower())
    
    def get_all_scrapers(self) -> Dict[str, BaseScraper]:
        """Get all registered scrapers"""
        return self._scrapers.copy()
    
    def get_search_terms(self) -> Dict[str, List[str]]:
        """Get search terms for all insurers"""
        return {
            insurer: scraper.get_search_terms()
            for insurer, scraper in self._scrapers.items()
        }

# Global registry
scraper_registry = ScraperRegistry()
