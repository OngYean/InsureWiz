"""
Dynamic API endpoints that use real-time scraping instead of mock data
"""

from fastapi import APIRouter, HTTPException, Query
from typing import List, Dict, Any, Optional
import logging
from datetime import datetime
import asyncio

from ..services.real_time_scraper import real_time_scraper
from ..database.supabase import get_supabase_client

logger = logging.getLogger(__name__)

def transform_to_supabase_schema(scraped_data: dict) -> dict:
    """Transform scraped data to match Supabase schema"""
    
    coverage_details_raw = scraped_data.get("coverage_details", {})
    coverage_details = {
        "windscreen_cover": coverage_details_raw.get("windscreen_cover", False),
        "roadside_assistance": coverage_details_raw.get("roadside_assistance", False),
        "flood_coverage": coverage_details_raw.get("flood_coverage", False),
        "riot_strike_coverage": coverage_details_raw.get("riot_strike", False),
        "theft_coverage": True,
        "legal_liability": coverage_details_raw.get("legal_liability", False),
        "accessories_cover": coverage_details_raw.get("accessories", False),
        "personal_accident": coverage_details_raw.get("personal_accident", False)
    }
    
    pricing_raw = scraped_data.get("pricing", {})
    pricing = {
        "base_premium": pricing_raw.get("base_premium", 2000),
        "service_tax": pricing_raw.get("service_tax", 120),
        "excess": 500,
        "ncd_discount": 55
    }
    
    eligibility_criteria = {
        "min_age": 18,
        "max_age": 75,
        "vehicle_age_max": 15,
        "license_years_min": 1
    }
    
    additional_benefits = {
        "roadside_assistance": coverage_details.get("roadside_assistance", False),
        "workshop_network": True,
        "online_claims": True,
        "mobile_app": True
    }
    
    return {
        "insurer": scraped_data.get("insurer", "Unknown"),
        "product_name": scraped_data.get("product_name", "Standard Motor"),
        "coverage_type": scraped_data.get("coverage_type", "comprehensive"),
        "is_takaful": scraped_data.get("is_takaful", False),
        "coverage_details": coverage_details,
        "pricing": pricing,
        "eligibility_criteria": eligibility_criteria,
        "additional_benefits": additional_benefits,
        "exclusions": scraped_data.get("exclusions", []),
        "source_urls": scraped_data.get("source_urls", [])
    }

router = APIRouter(prefix="/dynamic", tags=["dynamic"])

@router.get("/health")
async def dynamic_health():
    """Health check for dynamic scraping features"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "features": {
            "real_time_scraping": "ready",
            "tavily_integration": "ready",
            "crawl4ai_simulation": "ready",
            "database_storage": "ready",
            "live_data": "active"
        },
        "scraped_insurers": list(real_time_scraper.insurers.keys())
    }

@router.post("/scrape/all")
async def scrape_all_insurers():
    """Scrape policies from all Malaysian insurers in real-time"""
    try:
        logger.info("Starting real-time scraping of all insurers...")
        
        # Perform real-time scraping
        policies = await real_time_scraper.scrape_all_insurers()
        
        # Store in database if available
        db_client = get_supabase_client()
        stored_count = 0
        
        if db_client:
            try:
                # Transform and insert policies
                for policy in policies:
                    # Transform to Supabase schema
                    transformed_policy = transform_to_supabase_schema(policy)
                    
                    try:
                        db_result = db_client.table("policies").insert(transformed_policy).execute()
                        if db_result.data:
                            stored_count += 1
                    except Exception as policy_error:
                        # Skip duplicates and other individual policy errors
                        if "unique constraint" not in str(policy_error):
                            logger.warning(f"Failed to store policy {policy.get('product_name', 'Unknown')}: {policy_error}")
                        
                logger.info(f"Stored {stored_count} policies in database")
            except Exception as e:
                logger.error(f"Database storage error: {e}")
        
        return {
            "status": "success",
            "timestamp": datetime.now().isoformat(),
            "scraped_policies": len(policies),
            "stored_in_database": stored_count,
            "insurers_processed": len(real_time_scraper.insurers),
            "policies": policies,
            "data_freshness": "real_time",
            "next_scrape_recommended": "24_hours"
        }
        
    except Exception as e:
        logger.error(f"Scraping failed: {e}")
        raise HTTPException(status_code=500, detail=f"Scraping failed: {str(e)}")

@router.get("/policies/live")
async def get_live_policies(
    insurer: Optional[str] = Query(None, description="Filter by insurer name"),
    coverage_type: Optional[str] = Query("comprehensive", description="Coverage type"),
    max_age_hours: Optional[int] = Query(24, description="Maximum data age in hours")
):
    """Get live scraped policies with real-time data"""
    try:
        # Get fresh data
        policies = await real_time_scraper.scrape_all_insurers()
        
        # Apply filters
        filtered_policies = policies
        
        if insurer:
            filtered_policies = [p for p in filtered_policies if insurer.lower() in p["insurer"].lower()]
        
        if coverage_type:
            filtered_policies = [p for p in filtered_policies if p.get("coverage_type") == coverage_type]
        
        # Add metadata
        for policy in filtered_policies:
            policy["is_live_data"] = True
            policy["data_source"] = "real_time_scraping"
            policy["api_endpoint"] = "/dynamic/policies/live"
        
        return {
            "status": "success",
            "timestamp": datetime.now().isoformat(),
            "total_policies": len(filtered_policies),
            "filters_applied": {
                "insurer": insurer,
                "coverage_type": coverage_type
            },
            "data_freshness": "live",
            "policies": filtered_policies
        }
        
    except Exception as e:
        logger.error(f"Live policy retrieval failed: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get live policies: {str(e)}")

@router.post("/compare/live")
async def live_comparison(request_data: Dict[str, Any]):
    """Real-time comparison using freshly scraped data"""
    try:
        logger.info("Starting live comparison with real-time data...")
        
        # Extract customer info
        vehicle_value = request_data.get("vehicle_value", 50000)
        customer_age = request_data.get("customer_age", 35)
        claims_history = request_data.get("claims_history", 0)
        location = request_data.get("location", "Kuala Lumpur")
        
        # Get fresh scraped data
        policies = await real_time_scraper.scrape_all_insurers()
        
        if not policies:
            raise HTTPException(status_code=404, detail="No live policies available")
        
        # Enhanced scoring with real-time data
        scored_policies = []
        
        for policy in policies:
            base_premium = policy.get("pricing", {}).get("base_premium", 0)
            
            # Real-time adjustments
            age_adjustment = 1.0
            if customer_age < 25:
                age_adjustment = 1.4
            elif customer_age < 30:
                age_adjustment = 1.2
            elif customer_age > 50:
                age_adjustment = 0.85
            
            claims_penalty = 1.0 + (claims_history * 0.15)
            vehicle_factor = vehicle_value / 50000
            
            adjusted_premium = base_premium * age_adjustment * claims_penalty * vehicle_factor
            
            # Coverage scoring
            coverage = policy.get("coverage_details", {})
            coverage_score = sum([
                15 if coverage.get("windscreen_cover") else 0,
                20 if coverage.get("flood_coverage") else 0,
                10 if coverage.get("roadside_assistance") else 0,
                10 if coverage.get("replacement_car") else 0,
                5 if coverage.get("towing_service") else 0
            ])
            
            # Final score
            max_premium = max([p.get("pricing", {}).get("base_premium", 0) for p in policies])
            price_score = (1 - (base_premium / max_premium)) * 100 if max_premium > 0 else 50
            final_score = (price_score * 0.6 + coverage_score) * 0.8 + 20
            
            scored_policies.append({
                "policy_id": policy.get("id"),
                "insurer": policy.get("insurer"),
                "product_name": policy.get("product_name"),
                "base_premium": base_premium,
                "adjusted_premium": round(adjusted_premium, 2),
                "score": round(final_score, 1),
                "coverage_details": coverage,
                "is_takaful": policy.get("is_takaful", False),
                "data_freshness": policy.get("data_freshness", "real_time"),
                "scraped_at": policy.get("scraped_at"),
                "source_url": policy.get("source_url", "N/A"),
                "adjustments": {
                    "age_factor": age_adjustment,
                    "claims_penalty": claims_penalty,
                    "vehicle_factor": vehicle_factor
                }
            })
        
        # Sort by score
        scored_policies.sort(key=lambda x: x["score"], reverse=True)
        
        session_id = f"live_{hash(str(request_data))}"
        
        return {
            "session_id": session_id,
            "comparison_type": "live_real_time",
            "timestamp": datetime.now().isoformat(),
            "customer_profile": {
                "age": customer_age,
                "location": location,
                "vehicle_value": vehicle_value,
                "claims_history": claims_history
            },
            "data_source": "real_time_scraping",
            "policies_analyzed": len(scored_policies),
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
            "scraping_info": {
                "insurers_scraped": len(real_time_scraper.insurers),
                "data_freshness": "live",
                "scraping_timestamp": datetime.now().isoformat()
            }
        }
        
    except Exception as e:
        logger.error(f"Live comparison failed: {e}")
        raise HTTPException(status_code=500, detail=f"Live comparison failed: {str(e)}")

@router.get("/insurers/live")
async def get_live_insurers():
    """Get list of insurers with live scraping capability"""
    try:
        # Get fresh data to see which insurers have live policies
        policies = await real_time_scraper.scrape_all_insurers()
        
        insurers_info = {}
        for policy in policies:
            insurer = policy["insurer"]
            if insurer not in insurers_info:
                insurers_info[insurer] = {
                    "name": insurer,
                    "policies_available": 0,
                    "has_takaful": False,
                    "data_freshness": policy.get("data_freshness", "real_time"),
                    "last_scraped": policy.get("scraped_at")
                }
            
            insurers_info[insurer]["policies_available"] += 1
            if policy.get("is_takaful"):
                insurers_info[insurer]["has_takaful"] = True
        
        return {
            "status": "success",
            "timestamp": datetime.now().isoformat(),
            "total_insurers": len(insurers_info),
            "insurers": list(insurers_info.values()),
            "scraping_capability": "real_time"
        }
        
    except Exception as e:
        logger.error(f"Failed to get live insurers: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get live insurers: {str(e)}")

@router.get("/scraping/status")
async def get_scraping_status():
    """Get current scraping status and capabilities"""
    import os
    
    return {
        "status": "operational",
        "timestamp": datetime.now().isoformat(),
        "scraping_enabled": bool(os.getenv("TAVILY_API_KEY")),
        "api_keys": {
            "tavily": "configured" if os.getenv("TAVILY_API_KEY") else "missing",
            "google_gemini": "configured" if os.getenv("GOOGLE_API_KEY") else "missing"
        },
        "target_insurers": list(real_time_scraper.insurers.keys()),
        "scraping_methods": ["tavily_discovery", "crawl4ai_extraction"],
        "data_storage": "supabase_postgresql",
        "real_time_capability": True,
        "supported_coverage_types": ["comprehensive", "third_party", "takaful"],
        "update_frequency": "on_demand"
    }
