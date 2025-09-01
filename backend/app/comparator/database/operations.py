"""
Database operations for policy management and comparison sessions
"""

from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
import json
import logging
from uuid import uuid4

from ..models.policy import PolicyRecord, PolicySummary
from ..models.comparison import ComparisonResult
from .supabase import get_supabase_client

logger = logging.getLogger(__name__)

class PolicyOperations:
    """Database operations for policy management"""
    
    def __init__(self):
        self.client = get_supabase_client()
    
    async def insert_policy(self, policy_data: Dict[str, Any]) -> Optional[str]:
        """Insert a new policy record using the correct Supabase schema"""
        if not self.client:
            logger.error("Database client not available")
            return None
        
        try:
            # Transform to Supabase schema if needed
            if not self._is_supabase_format(policy_data):
                policy_data = self._transform_to_supabase_schema(policy_data)
            
            result = self.client.table("policies").insert(policy_data).execute()
            
            if result.data:
                policy_id = result.data[0]["id"]
                logger.info(f"Policy inserted successfully: {policy_id}")
                return policy_id
            else:
                logger.error("Failed to insert policy: No data returned")
                return None
                
        except Exception as e:
            logger.error(f"Error inserting policy: {e}")
            return None
    
    async def update_policy(self, policy_id: str, policy: PolicyRecord) -> bool:
        """Update an existing policy record"""
        if not self.client:
            logger.error("Database client not available")
            return False
        
        try:
            policy_data = {
                "insurer": policy.insurer,
                "product_name": policy.product_name,
                "is_takaful": policy.is_takaful,
                "coverage_type": policy.coverage_type.value,
                "valuation_method": policy.valuation_method.value if policy.valuation_method else None,
                "eligibility": policy.eligibility.dict(),
                "included_cover": policy.included_cover.dict(),
                "addons": policy.addons.dict(),
                "services": policy.services.dict(),
                "pricing_notes": policy.pricing_notes.dict(),
                "exclusions": policy.exclusions,
                "source_urls": policy.source_urls,
                "last_checked": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat()
            }
            
            result = self.client.table("policies").update(policy_data).eq("id", policy_id).execute()
            
            if result.data:
                logger.info(f"Policy updated successfully: {policy_id}")
                return True
            else:
                logger.error(f"Failed to update policy: {policy_id}")
                return False
                
        except Exception as e:
            logger.error(f"Error updating policy: {e}")
            return False
    
    def _is_supabase_format(self, data: Dict[str, Any]) -> bool:
        """Check if data is already in Supabase format"""
        required_fields = {"coverage_details", "pricing", "eligibility_criteria"}
        return all(field in data for field in required_fields)
    
    def _transform_to_supabase_schema(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Transform policy data to match Supabase schema"""
        
        # Extract coverage details
        coverage_details_raw = data.get("coverage_details", {})
        coverage_details = {
            "windscreen_cover": coverage_details_raw.get("windscreen_cover", False),
            "roadside_assistance": coverage_details_raw.get("roadside_assistance", False),
            "flood_coverage": coverage_details_raw.get("flood_coverage", False),
            "riot_strike_coverage": coverage_details_raw.get("riot_strike", False),
            "theft_coverage": True,  # Standard for comprehensive
            "legal_liability": coverage_details_raw.get("legal_liability", False),
            "accessories_cover": coverage_details_raw.get("accessories", False),
            "personal_accident": coverage_details_raw.get("personal_accident", False)
        }
        
        # Extract pricing
        pricing_raw = data.get("pricing", {})
        pricing = {
            "base_premium": pricing_raw.get("base_premium", 2000),
            "service_tax": pricing_raw.get("service_tax", 120),
            "excess": 500,
            "ncd_discount": 55
        }
        
        # Create eligibility criteria
        eligibility_criteria = {
            "min_age": 18,
            "max_age": 75,
            "vehicle_age_max": 15,
            "license_years_min": 1
        }
        
        # Additional benefits
        additional_benefits = {
            "roadside_assistance": coverage_details.get("roadside_assistance", False),
            "workshop_network": True,
            "online_claims": True,
            "mobile_app": True
        }
        
        return {
            "insurer": data.get("insurer", "Unknown"),
            "product_name": data.get("product_name", "Standard Motor"),
            "coverage_type": data.get("coverage_type", "comprehensive"),
            "is_takaful": data.get("is_takaful", False),
            "coverage_details": coverage_details,
            "pricing": pricing,
            "eligibility_criteria": eligibility_criteria,
            "additional_benefits": additional_benefits,
            "exclusions": data.get("exclusions", []),
            "source_urls": data.get("source_urls", [])
        }
    
    async def get_policy(self, policy_id: str) -> Optional[PolicyRecord]:
        """Get a policy by ID"""
        if not self.client:
            return None
        
        try:
            result = self.client.table("policies").select("*").eq("id", policy_id).execute()
            
            if result.data:
                return self._dict_to_policy(result.data[0])
            return None
            
        except Exception as e:
            logger.error(f"Error getting policy: {e}")
            return None
    
    async def get_policies(
        self,
        insurer: Optional[str] = None,
        coverage_type: Optional[str] = None,
        is_takaful: Optional[bool] = None,
        limit: int = 100
    ) -> List[PolicyRecord]:
        """Get policies with optional filters"""
        if not self.client:
            return []
        
        try:
            query = self.client.table("policies").select("*")
            
            if insurer:
                query = query.eq("insurer", insurer)
            if coverage_type:
                query = query.eq("coverage_type", coverage_type)
            if is_takaful is not None:
                query = query.eq("is_takaful", is_takaful)
            
            result = query.limit(limit).order("updated_at", desc=True).execute()
            
            return [self._dict_to_policy(row) for row in result.data]
            
        except Exception as e:
            logger.error(f"Error getting policies: {e}")
            return []
    
    async def get_policy_summaries(self) -> List[PolicySummary]:
        """Get lightweight policy summaries"""
        if not self.client:
            return []
        
        try:
            result = self.client.table("policies").select(
                "id, insurer, product_name, is_takaful, coverage_type, last_checked"
            ).order("updated_at", desc=True).execute()
            
            summaries = []
            for row in result.data:
                summaries.append(PolicySummary(
                    id=row["id"],
                    insurer=row["insurer"],
                    product_name=row["product_name"],
                    is_takaful=row["is_takaful"],
                    coverage_type=row["coverage_type"],
                    last_checked=datetime.fromisoformat(row["last_checked"]) if row["last_checked"] else None
                ))
            
            return summaries
            
        except Exception as e:
            logger.error(f"Error getting policy summaries: {e}")
            return []
    
    async def delete_policy(self, policy_id: str) -> bool:
        """Delete a policy by ID"""
        if not self.client:
            return False
        
        try:
            result = self.client.table("policies").delete().eq("id", policy_id).execute()
            logger.info(f"Policy deleted: {policy_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error deleting policy: {e}")
            return False
    
    def _dict_to_policy(self, data: Dict[str, Any]) -> PolicyRecord:
        """Convert database row to PolicyRecord"""
        return PolicyRecord(
            id=data["id"],
            insurer=data["insurer"],
            product_name=data["product_name"],
            is_takaful=data["is_takaful"],
            coverage_type=data["coverage_type"],
            valuation_method=data.get("valuation_method"),
            eligibility=data.get("eligibility", {}),
            included_cover=data.get("included_cover", {}),
            addons=data.get("addons", {}),
            services=data.get("services", {}),
            pricing_notes=data.get("pricing_notes", {}),
            exclusions=data.get("exclusions", []),
            source_urls=data.get("source_urls", []),
            last_checked=datetime.fromisoformat(data["last_checked"]) if data.get("last_checked") else None,
            created_at=datetime.fromisoformat(data["created_at"]) if data.get("created_at") else None,
            updated_at=datetime.fromisoformat(data["updated_at"]) if data.get("updated_at") else None
        )


class ComparisonOperations:
    """Database operations for comparison sessions"""
    
    def __init__(self):
        self.client = get_supabase_client()
    
    async def save_comparison(self, comparison: ComparisonResult) -> Optional[str]:
        """Save a comparison result"""
        if not self.client:
            logger.error("Database client not available")
            return None
        
        try:
            session_data = {
                "id": comparison.session_id,
                "customer_data": {
                    "name": comparison.customer_name,
                    "comparison_date": comparison.comparison_date.isoformat()
                },
                "comparison_results": comparison.dict(),
                "created_at": datetime.now().isoformat(),
                "expires_at": (datetime.now() + timedelta(days=30)).isoformat()
            }
            
            result = self.client.table("comparison_sessions").insert(session_data).execute()
            
            if result.data:
                logger.info(f"Comparison saved: {comparison.session_id}")
                return comparison.session_id
            return None
            
        except Exception as e:
            logger.error(f"Error saving comparison: {e}")
            return None
    
    async def get_comparison(self, session_id: str) -> Optional[ComparisonResult]:
        """Get a comparison result by session ID"""
        if not self.client:
            return None
        
        try:
            result = self.client.table("comparison_sessions").select("*").eq("id", session_id).execute()
            
            if result.data:
                data = result.data[0]
                comparison_data = data["comparison_results"]
                return ComparisonResult(**comparison_data)
            return None
            
        except Exception as e:
            logger.error(f"Error getting comparison: {e}")
            return None
    
    async def update_pdf_path(self, session_id: str, pdf_path: str) -> bool:
        """Update the PDF path for a comparison session"""
        if not self.client:
            return False
        
        try:
            result = self.client.table("comparison_sessions").update({
                "pdf_path": pdf_path
            }).eq("id", session_id).execute()
            
            return bool(result.data)
            
        except Exception as e:
            logger.error(f"Error updating PDF path: {e}")
            return False

# Global instances
policy_ops = PolicyOperations()
comparison_ops = ComparisonOperations()
