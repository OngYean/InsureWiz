"""
Simple API endpoints for testing the comparator
"""

from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any, Optional
import logging
from datetime import datetime

from ..database.simple_ops import (
    get_policies_simple, 
    get_insurers_simple, 
    save_comparison_simple,
    get_comparison_simple
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/simple", tags=["simple"])

@router.get("/health")
async def health_check():
    """Simple health check"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "insurance_comparator"
    }

@router.get("/policies")
async def get_policies(
    coverage_type: Optional[str] = None,
    insurer: Optional[str] = None
) -> List[Dict[str, Any]]:
    """Get insurance policies with optional filtering"""
    try:
        policies = await get_policies_simple(coverage_type, insurer)
        return policies
    except Exception as e:
        logger.error(f"Error getting policies: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve policies")

@router.get("/insurers")
async def get_insurers() -> List[str]:
    """Get list of available insurers"""
    try:
        insurers = await get_insurers_simple()
        return insurers
    except Exception as e:
        logger.error(f"Error getting insurers: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve insurers")

@router.post("/compare")
async def compare_policies(request_data: Dict[str, Any]):
    """Simple policy comparison"""
    try:
        # Extract basic info from request
        vehicle_type = request_data.get("vehicle_type", "private_car")
        coverage_type = request_data.get("coverage_type", "comprehensive")
        vehicle_value = request_data.get("vehicle_value", 50000)
        
        # Get relevant policies
        policies = await get_policies_simple(coverage_type=coverage_type)
        
        # Simple scoring
        results = []
        for policy in policies:
            base_premium = policy.get("pricing", {}).get("base_premium", 0)
            
            # Calculate rough premium based on vehicle value
            premium_rate = base_premium / 50000  # Assuming base is for 50k vehicle
            estimated_premium = premium_rate * vehicle_value
            
            # Simple score (lower premium = higher score)
            max_premium = max([p.get("pricing", {}).get("base_premium", 0) for p in policies])
            score = 100 - ((base_premium / max_premium) * 100) if max_premium > 0 else 50
            
            results.append({
                "policy_id": policy.get("id"),
                "insurer": policy.get("insurer"),
                "product_name": policy.get("product_name"),
                "estimated_premium": round(estimated_premium, 2),
                "score": round(score, 1),
                "coverage_details": policy.get("coverage_details", {}),
                "is_takaful": policy.get("is_takaful", False)
            })
        
        # Sort by score (highest first)
        results.sort(key=lambda x: x["score"], reverse=True)
        
        # Create session
        session_id = f"comp_{hash(str(request_data))}"
        comparison_data = {
            "customer_input": request_data,
            "policies_compared": results,
            "comparison_date": datetime.now().isoformat()
        }
        
        await save_comparison_simple(session_id, comparison_data)
        
        return {
            "session_id": session_id,
            "comparison_summary": {
                "total_policies": len(results),
                "best_policy": results[0] if results else None,
                "average_premium": sum(r["estimated_premium"] for r in results) / len(results) if results else 0
            },
            "policy_rankings": results
        }
        
    except Exception as e:
        logger.error(f"Error in comparison: {e}")
        raise HTTPException(status_code=500, detail="Failed to compare policies")

@router.get("/comparison/{session_id}")
async def get_comparison_result(session_id: str):
    """Get comparison result by session ID"""
    try:
        result = await get_comparison_simple(session_id)
        if not result:
            raise HTTPException(status_code=404, detail="Comparison session not found")
        return result
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting comparison: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve comparison")

@router.get("/stats")
async def get_stats():
    """Get simple statistics"""
    try:
        policies = await get_policies_simple()
        insurers = await get_insurers_simple()
        
        return {
            "total_policies": len(policies),
            "total_insurers": len(insurers),
            "coverage_types": list(set(p.get("coverage_type") for p in policies)),
            "takaful_count": len([p for p in policies if p.get("is_takaful")]),
            "conventional_count": len([p for p in policies if not p.get("is_takaful")])
        }
    except Exception as e:
        logger.error(f"Error getting stats: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve statistics")
