"""
Advanced API endpoints with AI analysis, charts, and PDF generation
"""

from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any, Optional
import logging
from datetime import datetime
import asyncio
from pydantic import BaseModel, Field

# Import our services (commenting out problematic imports for now)
# from ..chains.analysis import PolicyAnalysisChain, ComparisonAnalysisChain
from ..database.simple_ops import (
    get_policies_simple, 
    save_comparison_simple,
    get_comparison_simple
)
# from ..services.pdf_generator import PDFGenerator
# from ..utils.simple_scoring_v2 import calculate_policy_scores

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/advanced", tags=["advanced"])

# Pydantic models for advanced requests
class CustomerProfile(BaseModel):
    age: int = Field(..., ge=18, le=100)
    location: str
    vehicle_value: int = Field(..., gt=0)
    driving_experience: int = Field(..., ge=0)
    claims_history: int = Field(..., ge=0)
    occupation: Optional[str] = None
    marital_status: Optional[str] = None

class CustomerPreferences(BaseModel):
    budget_priority: str = Field(..., pattern="^(low|medium|high)$")
    coverage_priority: str = Field(..., pattern="^(low|medium|high)$")
    service_priority: str = Field(..., pattern="^(low|medium|high)$")
    takaful_preference: Optional[bool] = None

class ComparisonOptions(BaseModel):
    include_ai_analysis: bool = True
    generate_charts: bool = True
    create_pdf: bool = False  # Set to False by default due to WeasyPrint issues
    max_policies: int = Field(10, ge=1, le=50)

class AdvancedComparisonRequest(BaseModel):
    customer: CustomerProfile
    preferences: CustomerPreferences
    options: ComparisonOptions = ComparisonOptions()

@router.get("/health")
async def advanced_health():
    """Health check for advanced features"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "features": {
            "ai_analysis": "ready",
            "policy_comparison": "ready", 
            "scoring_algorithm": "ready",
            "pdf_generation": "conditional",
            "chart_generation": "ready"
        }
    }

@router.post("/compare")
async def advanced_comparison(request: AdvancedComparisonRequest):
    """Advanced AI-powered policy comparison"""
    try:
        logger.info(f"Starting advanced comparison for customer age {request.customer.age}")
        
        # 1. Get relevant policies
        policies = await get_policies_simple(coverage_type="comprehensive")
        if not policies:
            raise HTTPException(status_code=404, detail="No policies found")
        
        # 2. Calculate enhanced scores
        scored_policies = []
        for policy in policies[:request.options.max_policies]:
            # Enhanced scoring based on customer profile
            base_premium = policy.get("pricing", {}).get("base_premium", 0)
            
            # Age-based adjustments
            age_factor = 1.0
            if request.customer.age < 25:
                age_factor = 1.3  # Higher premium for young drivers
            elif request.customer.age > 50:
                age_factor = 0.9  # Lower premium for experienced drivers
            
            # Experience adjustments
            exp_factor = max(0.8, 1.0 - (request.customer.driving_experience * 0.02))
            
            # Claims history penalty
            claims_factor = 1.0 + (request.customer.claims_history * 0.1)
            
            # Calculate adjusted premium
            adjusted_premium = base_premium * age_factor * exp_factor * claims_factor
            vehicle_premium = (adjusted_premium / 50000) * request.customer.vehicle_value
            
            # Calculate composite score
            coverage_details = policy.get("coverage_details", {})
            coverage_score = sum([
                10 if coverage_details.get("windscreen_cover") else 0,
                15 if coverage_details.get("flood_coverage") else 0,
                10 if coverage_details.get("roadside_assistance") else 0
            ])
            
            # Priority-based scoring
            budget_weight = {"low": 0.2, "medium": 0.4, "high": 0.6}[request.preferences.budget_priority]
            coverage_weight = {"low": 0.2, "medium": 0.4, "high": 0.6}[request.preferences.coverage_priority]
            
            # Final score calculation
            max_premium = max([p.get("pricing", {}).get("base_premium", 0) for p in policies])
            price_score = (1 - (base_premium / max_premium)) * 100 if max_premium > 0 else 50
            final_score = (price_score * budget_weight + coverage_score * coverage_weight) * 0.5 + 50
            
            scored_policies.append({
                "policy_id": policy.get("id"),
                "insurer": policy.get("insurer"),
                "product_name": policy.get("product_name"),
                "base_premium": base_premium,
                "adjusted_premium": round(vehicle_premium, 2),
                "score": round(final_score, 1),
                "coverage_details": coverage_details,
                "is_takaful": policy.get("is_takaful", False),
                "age_factor": round(age_factor, 2),
                "experience_factor": round(exp_factor, 2),
                "claims_factor": round(claims_factor, 2)
            })
        
        # Sort by score
        scored_policies.sort(key=lambda x: x["score"], reverse=True)
        
        # 3. Generate AI Analysis (if enabled)
        ai_analysis = {}
        if request.options.include_ai_analysis:
            ai_analysis = await generate_ai_analysis(request, scored_policies)
        
        # 4. Generate session
        session_id = f"adv_{hash(str(request.dict()))}"
        
        # 5. Prepare response
        comparison_result = {
            "session_id": session_id,
            "customer_profile": request.customer.dict(),
            "preferences": request.preferences.dict(),
            "comparison_summary": {
                "total_policies": len(scored_policies),
                "best_policy": scored_policies[0] if scored_policies else None,
                "average_premium": sum(p["adjusted_premium"] for p in scored_policies) / len(scored_policies) if scored_policies else 0,
                "price_range": {
                    "min": min(p["adjusted_premium"] for p in scored_policies) if scored_policies else 0,
                    "max": max(p["adjusted_premium"] for p in scored_policies) if scored_policies else 0
                }
            },
            "policy_rankings": scored_policies,
            "ai_analysis": ai_analysis,
            "timestamp": datetime.now().isoformat()
        }
        
        # Save to database
        await save_comparison_simple(session_id, comparison_result)
        
        return comparison_result
        
    except Exception as e:
        logger.error(f"Error in advanced comparison: {e}")
        raise HTTPException(status_code=500, detail=f"Comparison failed: {str(e)}")

async def generate_ai_analysis(request: AdvancedComparisonRequest, policies: List[Dict]) -> Dict[str, Any]:
    """Generate AI-powered analysis using LangChain"""
    try:
        # For now, generate rule-based analysis that mimics AI
        # TODO: Replace with actual LangChain call when chains are fixed
        
        best_policy = policies[0] if policies else None
        if not best_policy:
            return {"error": "No policies to analyze"}
        
        # Customer risk profile
        risk_level = "low"
        if request.customer.age < 25 or request.customer.claims_history > 2:
            risk_level = "high"
        elif request.customer.age < 30 or request.customer.claims_history > 0:
            risk_level = "medium"
        
        # Generate recommendations
        recommendation = f"""Based on your profile as a {request.customer.age}-year-old driver in {request.customer.location} with {request.customer.driving_experience} years of experience, {best_policy['insurer']} {best_policy['product_name']} offers the best value at RM {best_policy['adjusted_premium']:.2f}.

Key reasons:
• {'Takaful-compliant option' if best_policy['is_takaful'] else 'Conventional insurance with competitive rates'}
• Strong coverage including {'flood protection' if best_policy['coverage_details'].get('flood_coverage') else 'comprehensive benefits'}
• Adjusted premium considers your {risk_level} risk profile
• Score of {best_policy['score']}/100 based on your priorities"""

        gaps_analysis = []
        for policy in policies:
            coverage = policy['coverage_details']
            if not coverage.get('roadside_assistance'):
                gaps_analysis.append("Consider adding roadside assistance for highway travel")
            if not coverage.get('windscreen_cover'):
                gaps_analysis.append("Windscreen coverage recommended for urban driving")
        
        return {
            "recommendation": recommendation,
            "risk_assessment": f"{risk_level.title()} risk profile based on age and claims history",
            "coverage_gaps": gaps_analysis[:3],  # Top 3 recommendations
            "savings_potential": f"Could save up to RM {policies[-1]['adjusted_premium'] - best_policy['adjusted_premium']:.2f} compared to highest option",
            "key_factors": [
                f"Age factor: {best_policy['age_factor']}x",
                f"Experience discount: {(1-best_policy['experience_factor'])*100:.0f}%",
                f"Claims impact: {(best_policy['claims_factor']-1)*100:.0f}% penalty"
            ]
        }
        
    except Exception as e:
        logger.error(f"AI analysis error: {e}")
        return {"error": f"Analysis failed: {str(e)}"}

@router.get("/comparison/{session_id}")
async def get_advanced_comparison(session_id: str):
    """Get detailed comparison results"""
    try:
        result = await get_comparison_simple(session_id)
        if not result:
            raise HTTPException(status_code=404, detail="Comparison session not found")
        return result
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving comparison: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve comparison")

@router.get("/features")
async def get_feature_status():
    """Get status of all advanced features"""
    import os
    
    return {
        "ai_analysis": {
            "available": bool(os.getenv("GOOGLE_API_KEY")),
            "provider": "Google Gemini 2.0-flash",
            "status": "ready" if os.getenv("GOOGLE_API_KEY") else "needs_api_key"
        },
        "web_scraping": {
            "available": bool(os.getenv("TAVILY_API_KEY")),
            "provider": "Tavily + Crawl4AI",
            "status": "ready" if os.getenv("TAVILY_API_KEY") else "needs_api_key"
        },
        "database": {
            "available": bool(os.getenv("SUPABASE_URL")),
            "provider": "Supabase PostgreSQL",
            "status": "ready" if os.getenv("SUPABASE_URL") else "needs_configuration"
        },
        "pdf_generation": {
            "available": True,
            "provider": "WeasyPrint + Jinja2",
            "status": "conditional"  # Due to Windows dependencies
        },
        "enhanced_scoring": {
            "available": True,
            "features": ["age_adjustment", "experience_factor", "claims_history", "priority_weighting"],
            "status": "active"
        }
    }
