"""
Data normalization service for converting scraped content to structured PolicyRecord objects
"""

import logging
from typing import List, Dict, Any, Optional
from datetime import datetime

from ..models.policy import PolicyRecord
from ..scrapers.base import scraper_registry
from ..chains.extraction import multi_extraction_chain

logger = logging.getLogger(__name__)

class DataNormalizer:
    """Service for normalizing scraped insurance data into PolicyRecord objects"""
    
    def __init__(self):
        self.extraction_chain = multi_extraction_chain
    
    async def normalize_crawled_data(self, crawled_data: Dict[str, Dict[str, str]]) -> List[PolicyRecord]:
        """Normalize all crawled data into PolicyRecord objects"""
        all_policies = []
        
        for insurer, url_content_map in crawled_data.items():
            logger.info(f"Normalizing data for {insurer}...")
            
            try:
                policies = await self._normalize_insurer_data(insurer, url_content_map)
                all_policies.extend(policies)
                
                logger.info(f"Normalized {len(policies)} policies for {insurer}")
                
            except Exception as e:
                logger.error(f"Error normalizing data for {insurer}: {e}")
                continue
        
        logger.info(f"Total normalized policies: {len(all_policies)}")
        return all_policies
    
    async def _normalize_insurer_data(self, insurer: str, url_content_map: Dict[str, str]) -> List[PolicyRecord]:
        """Normalize data for a specific insurer"""
        policies = []
        
        # Get the appropriate scraper for this insurer
        scraper = scraper_registry.get_scraper(insurer)
        
        for url, content in url_content_map.items():
            if not content.strip():
                logger.warning(f"Empty content for {url}")
                continue
            
            try:
                # Use scraper-specific parsing if available
                if scraper:
                    parsed_policies = scraper.parse_content(content, url)
                    policies.extend(parsed_policies)
                else:
                    # Fall back to LangChain extraction
                    parsed_policies = self.extraction_chain.extract_policies(content, url, insurer)
                    policies.extend(parsed_policies)
                
            except Exception as e:
                logger.error(f"Error parsing content from {url}: {e}")
                continue
        
        # Post-process policies
        processed_policies = self._post_process_policies(policies, insurer)
        return processed_policies
    
    def _post_process_policies(self, policies: List[PolicyRecord], insurer: str) -> List[PolicyRecord]:
        """Post-process policies for quality and consistency"""
        processed = []
        
        for policy in policies:
            try:
                # Ensure insurer name consistency
                policy.insurer = insurer
                
                # Set timestamps
                policy.last_checked = datetime.now()
                if not policy.created_at:
                    policy.created_at = datetime.now()
                policy.updated_at = datetime.now()
                
                # Validate policy
                if self._validate_policy_quality(policy):
                    processed.append(policy)
                else:
                    logger.warning(f"Policy failed quality check: {policy.product_name}")
                
            except Exception as e:
                logger.error(f"Error post-processing policy: {e}")
                continue
        
        return processed
    
    def _validate_policy_quality(self, policy: PolicyRecord) -> bool:
        """Validate policy data quality"""
        # Check required fields
        if not policy.insurer or not policy.product_name:
            return False
        
        if not policy.coverage_type:
            return False
        
        # Check for minimum content
        has_coverage_info = any([
            policy.included_cover.theft,
            policy.included_cover.flood,
            policy.included_cover.windscreen,
            policy.included_cover.personal_accident
        ])
        
        has_service_info = any([
            policy.services.roadside_assist_24_7,
            policy.services.digital_claims,
            policy.services.mobile_app,
            policy.services.panel_workshop_count is not None
        ])
        
        # Must have either coverage or service information
        if not (has_coverage_info or has_service_info):
            logger.debug(f"Policy {policy.product_name} lacks sufficient detail")
            return False
        
        return True
    
    def merge_duplicate_policies(self, policies: List[PolicyRecord]) -> List[PolicyRecord]:
        """Merge duplicate policies from different sources"""
        # Group by insurer and product name
        policy_groups = {}
        
        for policy in policies:
            key = (policy.insurer.lower(), policy.product_name.lower())
            if key not in policy_groups:
                policy_groups[key] = []
            policy_groups[key].append(policy)
        
        merged_policies = []
        
        for key, group in policy_groups.items():
            if len(group) == 1:
                merged_policies.append(group[0])
            else:
                # Merge multiple policies
                merged = self._merge_policy_group(group)
                if merged:
                    merged_policies.append(merged)
        
        logger.info(f"Merged {len(policies)} policies into {len(merged_policies)} unique policies")
        return merged_policies
    
    def _merge_policy_group(self, policies: List[PolicyRecord]) -> Optional[PolicyRecord]:
        """Merge a group of similar policies"""
        if not policies:
            return None
        
        # Use the most recent policy as base
        base_policy = max(policies, key=lambda p: p.last_checked or datetime.min)
        
        # Merge source URLs
        all_urls = set()
        for policy in policies:
            all_urls.update(policy.source_urls)
        base_policy.source_urls = list(all_urls)
        
        # Merge coverage information (OR logic - if any policy has it, include it)
        for policy in policies:
            if policy != base_policy:
                self._merge_coverage(base_policy, policy)
                self._merge_services(base_policy, policy)
                self._merge_addons(base_policy, policy)
                self._merge_pricing_notes(base_policy, policy)
        
        return base_policy
    
    def _merge_coverage(self, base: PolicyRecord, other: PolicyRecord):
        """Merge coverage information"""
        base.included_cover.flood = base.included_cover.flood or other.included_cover.flood
        base.included_cover.theft = base.included_cover.theft or other.included_cover.theft
        base.included_cover.riot_strike = base.included_cover.riot_strike or other.included_cover.riot_strike
        base.included_cover.windscreen = base.included_cover.windscreen or other.included_cover.windscreen
        base.included_cover.personal_accident = base.included_cover.personal_accident or other.included_cover.personal_accident
        base.included_cover.accessories = base.included_cover.accessories or other.included_cover.accessories
        base.included_cover.natural_disaster = base.included_cover.natural_disaster or other.included_cover.natural_disaster
        base.included_cover.ehailing_coverage = base.included_cover.ehailing_coverage or other.included_cover.ehailing_coverage
        base.included_cover.passenger_liability = base.included_cover.passenger_liability or other.included_cover.passenger_liability
        base.included_cover.legal_liability = base.included_cover.legal_liability or other.included_cover.legal_liability
    
    def _merge_services(self, base: PolicyRecord, other: PolicyRecord):
        """Merge service information"""
        base.services.roadside_assist_24_7 = base.services.roadside_assist_24_7 or other.services.roadside_assist_24_7
        base.services.claim_fast_track = base.services.claim_fast_track or other.services.claim_fast_track
        base.services.digital_claims = base.services.digital_claims or other.services.digital_claims
        base.services.mobile_app = base.services.mobile_app or other.services.mobile_app
        base.services.online_portal = base.services.online_portal or other.services.online_portal
        
        # Use more specific values where available
        if other.services.roadside_assist_sla and not base.services.roadside_assist_sla:
            base.services.roadside_assist_sla = other.services.roadside_assist_sla
        
        if other.services.panel_workshop_count and not base.services.panel_workshop_count:
            base.services.panel_workshop_count = other.services.panel_workshop_count
    
    def _merge_addons(self, base: PolicyRecord, other: PolicyRecord):
        """Merge addon information"""
        # For addon dictionaries, merge if base is empty
        if other.addons.ncd_protection and not base.addons.ncd_protection:
            base.addons.ncd_protection = other.addons.ncd_protection
        
        if other.addons.key_replacement and not base.addons.key_replacement:
            base.addons.key_replacement = other.addons.key_replacement
        
        if other.addons.courtesy_car and not base.addons.courtesy_car:
            base.addons.courtesy_car = other.addons.courtesy_car
    
    def _merge_pricing_notes(self, base: PolicyRecord, other: PolicyRecord):
        """Merge pricing information"""
        # Merge lists, avoiding duplicates
        base.pricing_notes.rebates = list(set(base.pricing_notes.rebates + other.pricing_notes.rebates))
        base.pricing_notes.cashback = list(set(base.pricing_notes.cashback + other.pricing_notes.cashback))
        base.pricing_notes.bundling_discounts = list(set(base.pricing_notes.bundling_discounts + other.pricing_notes.bundling_discounts))
        base.pricing_notes.loyalty_benefits = list(set(base.pricing_notes.loyalty_benefits + other.pricing_notes.loyalty_benefits))

# Global instance
data_normalizer = DataNormalizer()
