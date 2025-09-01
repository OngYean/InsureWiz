"""
Simple database operations without complex model dependencies
"""

from typing import List, Dict, Any, Optional
import json
import logging

logger = logging.getLogger(__name__)

def get_sample_policies() -> List[Dict[str, Any]]:
    """Get sample policies for testing"""
    return [
        {
            "id": "1",
            "insurer": "Zurich Malaysia",
            "product_name": "Z-Driver",
            "coverage_type": "comprehensive",
            "is_takaful": False,
            "pricing": {"base_premium": 2500, "service_tax": 300},
            "coverage_details": {
                "windscreen_cover": True,
                "roadside_assistance": True,
                "flood_coverage": True
            }
        },
        {
            "id": "2", 
            "insurer": "Etiqa",
            "product_name": "Private Car Takaful",
            "coverage_type": "comprehensive",
            "is_takaful": True,
            "pricing": {"base_premium": 2200, "service_tax": 264},
            "coverage_details": {
                "windscreen_cover": True,
                "flood_coverage": True,
                "roadside_assistance": False
            }
        },
        {
            "id": "3",
            "insurer": "Allianz General",
            "product_name": "MotorSafe",
            "coverage_type": "comprehensive",
            "is_takaful": False,
            "pricing": {"base_premium": 2800, "service_tax": 336},
            "coverage_details": {
                "windscreen_cover": True,
                "roadside_assistance": True,
                "flood_coverage": False
            }
        }
    ]

async def get_policies_simple(coverage_type: str = None, insurer: str = None) -> List[Dict[str, Any]]:
    """Get policies with simple filtering"""
    policies = get_sample_policies()
    
    if coverage_type:
        policies = [p for p in policies if p.get("coverage_type") == coverage_type]
    
    if insurer:
        policies = [p for p in policies if p.get("insurer") == insurer]
    
    logger.info(f"Retrieved {len(policies)} policies")
    return policies

async def get_insurers_simple() -> List[str]:
    """Get list of insurers"""
    policies = get_sample_policies()
    insurers = list(set(p["insurer"] for p in policies))
    return sorted(insurers)

async def save_comparison_simple(session_id: str, comparison_data: Dict[str, Any]) -> bool:
    """Save comparison result (mock implementation)"""
    try:
        logger.info(f"Saved comparison session {session_id}")
        return True
    except Exception as e:
        logger.error(f"Failed to save comparison: {e}")
        return False

async def get_comparison_simple(session_id: str) -> Optional[Dict[str, Any]]:
    """Get comparison result (mock implementation)"""
    try:
        logger.info(f"Retrieved comparison session {session_id}")
        return {"session_id": session_id, "status": "completed"}
    except Exception as e:
        logger.error(f"Failed to get comparison: {e}")
        return None
