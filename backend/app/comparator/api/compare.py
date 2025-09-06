"""
API endpoints for policy comparison and analysis
"""

from fastapi import APIRouter, HTTPException, Depends
from typing import List, Dict, Any, Optional
import logging
from datetime import datetime

from ..models.policy import CustomerInput
from ..models.comparison import ComparisonResult
from ..models.comparison import QuickCompareRequest, DetailedCompareRequest
from ..services.comparator import policy_comparator
from ..services.normalizer import data_normalizer
from ..database.operations import policy_ops, comparison_ops
from ..utils.simple_scoring_v2 import ScoreWeights
from ..utils.compliance import compliance_manager

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/comparator/compare", tags=["comparison"])

@router.post("/quick", response_model=ComparisonResult)
async def quick_compare(request: QuickCompareRequest):
    """Quick policy comparison with minimal requirements"""
    try:
        # Get available policies from database
        policies = await policy_ops.get_policies_by_coverage_type(request.coverage_type)
        
        if not policies:
            raise HTTPException(
                status_code=404, 
                detail=f"No policies found for coverage type: {request.coverage_type}"
            )
        
        # Apply basic filters
        filtered_policies = []
        for policy in policies:
            # Check Takaful preference
            if request.prefer_takaful is not None and policy.is_takaful != request.prefer_takaful:
                continue
            
            # Check price range
            if (request.max_price and 
                policy.pricing and 
                policy.pricing.get('base_premium', float('inf')) > request.max_price):
                continue
            
            filtered_policies.append(policy)
        
        if not filtered_policies:
            raise HTTPException(
                status_code=404,
                detail="No policies match your criteria"
            )
        
        # Create basic customer input
        customer_input = CustomerInput(
            vehicle_type=request.vehicle_type,
            coverage_preference=request.coverage_type,
            price_range_max=request.max_price,
            prefers_takaful=request.prefer_takaful or False
        )
        
        # Perform comparison
        comparison_result = await policy_comparator.compare_policies(
            customer_input=customer_input,
            policies=filtered_policies,
            weights=ScoreWeights()  # Use default weights
        )
        
        # Store comparison session
        session_id = await comparison_ops.create_comparison_session(
            customer_input=customer_input,
            comparison_result=comparison_result
        )
        
        comparison_result.session_id = session_id
        
        return comparison_result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in quick comparison: {e}")
        raise HTTPException(status_code=500, detail=f"Comparison failed: {str(e)}")

@router.post("/detailed", response_model=ComparisonResult)
async def detailed_compare(request: DetailedCompareRequest):
    """Detailed policy comparison with full customer profile"""
    try:
        # Validate customer input
        compliance_issues = compliance_manager.validate_customer_data(request.customer_input)
        if compliance_issues:
            raise HTTPException(
                status_code=400,
                detail=f"Customer data validation failed: {'; '.join(compliance_issues)}"
            )
        
        # Get policies from database
        policies = await policy_ops.get_policies_by_coverage_type(
            request.customer_input.coverage_preference
        )
        
        if not policies:
            raise HTTPException(
                status_code=404,
                detail=f"No policies found for coverage type: {request.customer_input.coverage_preference}"
            )
        
        # Apply eligibility filters
        eligible_policies = []
        for policy in policies:
            # Check Takaful preference
            if request.customer_input.prefers_takaful and not policy.is_takaful:
                continue
            
            # Check price range
            if (request.customer_input.price_range_max and 
                policy.pricing and 
                policy.pricing.get('base_premium', 0) > request.customer_input.price_range_max):
                continue
            
            # Check vehicle eligibility
            if policy.eligibility_criteria:
                vehicle_eligible = True
                min_age = policy.eligibility_criteria.get('vehicle_age_max')
                if min_age and request.customer_input.vehicle_age and request.customer_input.vehicle_age > min_age:
                    vehicle_eligible = False
                
                if vehicle_eligible:
                    eligible_policies.append(policy)
            else:
                eligible_policies.append(policy)
        
        if not eligible_policies:
            raise HTTPException(
                status_code=404,
                detail="No policies match your detailed criteria"
            )
        
        # Use custom weights if provided
        weights = request.weights or ScoreWeights()
        
        # Perform detailed comparison
        comparison_result = await policy_comparator.compare_policies(
            customer_input=request.customer_input,
            policies=eligible_policies,
            weights=weights
        )
        
        # Store comparison session
        session_id = await comparison_ops.create_comparison_session(
            customer_input=request.customer_input,
            comparison_result=comparison_result
        )
        
        comparison_result.session_id = session_id
        
        return comparison_result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in detailed comparison: {e}")
        raise HTTPException(status_code=500, detail=f"Detailed comparison failed: {str(e)}")

@router.get("/session/{session_id}", response_model=ComparisonResult)
async def get_comparison_session(session_id: str):
    """Retrieve a saved comparison session"""
    try:
        session = await comparison_ops.get_comparison_session(session_id)
        
        if not session:
            raise HTTPException(status_code=404, detail="Comparison session not found")
        
        return session
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving comparison session: {e}")
        raise HTTPException(status_code=500, detail=f"Session retrieval failed: {str(e)}")

@router.post("/recompare/{session_id}")
async def recompare_with_new_weights(session_id: str, weights: ScoreWeights):
    """Recompare policies from a saved session with new weights"""
    try:
        # Get original session
        session = await comparison_ops.get_comparison_session(session_id)
        
        if not session:
            raise HTTPException(status_code=404, detail="Comparison session not found")
        
        # Get original policies (you might need to store policy IDs in session)
        policies = await policy_ops.get_policies_by_coverage_type(
            session.customer_input.coverage_preference
        )
        
        # Recompare with new weights
        new_comparison = await policy_comparator.compare_policies(
            customer_input=session.customer_input,
            policies=policies,
            weights=weights
        )
        
        # Update session
        await comparison_ops.update_comparison_session(session_id, new_comparison)
        
        return {
            "status": "success",
            "message": "Comparison updated with new weights",
            "comparison": new_comparison
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in recomparison: {e}")
        raise HTTPException(status_code=500, detail=f"Recomparison failed: {str(e)}")

@router.get("/policies")
async def get_available_policies(
    coverage_type: Optional[str] = None,
    insurer: Optional[str] = None,
    is_takaful: Optional[bool] = None,
    limit: int = 50
):
    """Get available policies with optional filters"""
    try:
        policies = await policy_ops.get_filtered_policies(
            coverage_type=coverage_type,
            insurer=insurer,
            is_takaful=is_takaful,
            limit=limit
        )
        
        return {
            "status": "success",
            "count": len(policies),
            "policies": [
                {
                    "id": policy.id,
                    "insurer": policy.insurer,
                    "product_name": policy.product_name,
                    "coverage_type": policy.coverage_type,
                    "is_takaful": policy.is_takaful,
                    "base_premium": policy.pricing.get('base_premium') if policy.pricing else None,
                    "last_updated": policy.last_updated
                }
                for policy in policies
            ]
        }
        
    except Exception as e:
        logger.error(f"Error getting policies: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to retrieve policies: {str(e)}")

@router.get("/insurers")
async def get_available_insurers():
    """Get list of available insurers"""
    try:
        insurers = await policy_ops.get_unique_insurers()
        
        return {
            "status": "success",
            "insurers": insurers
        }
        
    except Exception as e:
        logger.error(f"Error getting insurers: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to retrieve insurers: {str(e)}")

@router.get("/stats")
async def get_comparison_stats():
    """Get comparison statistics"""
    try:
        # Get policy count by insurer
        policies_by_insurer = await policy_ops.get_policy_count_by_insurer()
        
        # Get comparison session count
        total_sessions = await comparison_ops.get_session_count()
        
        # Get recent sessions
        recent_sessions = await comparison_ops.get_recent_sessions(limit=5)
        
        return {
            "status": "success",
            "stats": {
                "total_policies": sum(policies_by_insurer.values()),
                "policies_by_insurer": policies_by_insurer,
                "total_comparison_sessions": total_sessions,
                "recent_sessions": len(recent_sessions)
            }
        }
        
    except Exception as e:
        logger.error(f"Error getting comparison stats: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to retrieve stats: {str(e)}")
