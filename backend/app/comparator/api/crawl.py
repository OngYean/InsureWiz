"""
API endpoints for web crawling and data extraction
"""

from fastapi import APIRouter, HTTPException, BackgroundTasks
from typing import List, Dict, Any, Optional
import logging

from ..services.crawler import crawler_service
from ..services.normalizer import data_normalizer
from ..database.operations import policy_ops
from ..scrapers.base import scraper_registry

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/comparator/crawl", tags=["crawling"])

@router.post("/discover")
async def discover_urls():
    """Discover insurance company URLs using Tavily API"""
    try:
        # Get search terms from all registered scrapers
        search_terms = scraper_registry.get_search_terms()
        
        # Discover URLs
        crawl_results = await crawler_service.discover_and_crawl(search_terms)
        
        # Count results
        total_urls = sum(len(urls) for urls in crawl_results.values())
        
        return {
            "status": "success",
            "message": f"Discovered content from {total_urls} URLs across {len(crawl_results)} insurers",
            "results": {
                insurer: {
                    "url_count": len(content_map),
                    "urls": list(content_map.keys())
                }
                for insurer, content_map in crawl_results.items()
            }
        }
        
    except Exception as e:
        logger.error(f"Error in URL discovery: {e}")
        raise HTTPException(status_code=500, detail=f"URL discovery failed: {str(e)}")

@router.post("/extract")
async def extract_and_normalize(background_tasks: BackgroundTasks):
    """Extract and normalize policy data from discovered URLs"""
    try:
        # Get search terms and discover URLs
        search_terms = scraper_registry.get_search_terms()
        crawl_results = await crawler_service.discover_and_crawl(search_terms)
        
        if not crawl_results:
            raise HTTPException(status_code=404, detail="No content found for extraction")
        
        # Normalize the crawled data
        policies = await data_normalizer.normalize_crawled_data(crawl_results)
        
        if not policies:
            raise HTTPException(status_code=404, detail="No policies could be extracted from crawled content")
        
        # Merge duplicate policies
        unique_policies = data_normalizer.merge_duplicate_policies(policies)
        
        # Store policies in background
        background_tasks.add_task(store_policies_background, unique_policies)
        
        return {
            "status": "success",
            "message": f"Extracted and normalized {len(unique_policies)} unique policies",
            "policies": [
                {
                    "insurer": policy.insurer,
                    "product_name": policy.product_name,
                    "coverage_type": policy.coverage_type,
                    "is_takaful": policy.is_takaful,
                    "source_urls": policy.source_urls
                }
                for policy in unique_policies
            ]
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in data extraction: {e}")
        raise HTTPException(status_code=500, detail=f"Data extraction failed: {str(e)}")

@router.post("/urls")
async def crawl_specific_urls(urls: List[str], background_tasks: BackgroundTasks):
    """Crawl specific URLs and extract policy data"""
    try:
        if not urls:
            raise HTTPException(status_code=400, detail="No URLs provided")
        
        if len(urls) > 10:
            raise HTTPException(status_code=400, detail="Maximum 10 URLs allowed per request")
        
        # Crawl the specified URLs
        content_results = await crawler_service.crawl_specific_urls(urls)
        
        # Group by insurer (basic detection)
        insurer_content = {}
        for url, content in content_results.items():
            insurer = detect_insurer_from_url(url)
            if insurer not in insurer_content:
                insurer_content[insurer] = {}
            insurer_content[insurer][url] = content
        
        # Normalize the data
        policies = await data_normalizer.normalize_crawled_data(insurer_content)
        
        # Store policies in background
        if policies:
            background_tasks.add_task(store_policies_background, policies)
        
        return {
            "status": "success",
            "message": f"Crawled {len(content_results)} URLs and extracted {len(policies)} policies",
            "results": content_results,
            "policies": [
                {
                    "insurer": policy.insurer,
                    "product_name": policy.product_name,
                    "coverage_type": policy.coverage_type
                }
                for policy in policies
            ]
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error crawling URLs: {e}")
        raise HTTPException(status_code=500, detail=f"URL crawling failed: {str(e)}")

@router.get("/status")
async def get_crawling_status():
    """Get status of crawling capabilities"""
    try:
        # Check registered scrapers
        scrapers = scraper_registry.get_all_scrapers()
        
        # Test sample URLs if available
        sample_urls = crawler_service.get_sample_urls()
        
        return {
            "status": "operational",
            "registered_scrapers": list(scrapers.keys()),
            "sample_urls_available": len(sample_urls),
            "tavily_api_available": bool(crawler_service.tavily.api_key),
            "crawl4ai_available": True  # Stub - would check actual availability
        }
        
    except Exception as e:
        logger.error(f"Error checking crawling status: {e}")
        raise HTTPException(status_code=500, detail=f"Status check failed: {str(e)}")

def detect_insurer_from_url(url: str) -> str:
    """Detect insurer from URL"""
    url_lower = url.lower()
    
    if 'zurich.com' in url_lower:
        return 'Zurich Malaysia'
    elif 'etiqa.com' in url_lower:
        return 'Etiqa'
    elif 'allianz.com' in url_lower:
        return 'Allianz General Insurance Malaysia'
    elif 'axa.com' in url_lower:
        return 'AXA Affin General'
    elif 'generali.com' in url_lower:
        return 'Generali Malaysia'
    elif 'libertyinsurance.com' in url_lower:
        return 'Liberty Insurance'
    elif 'amgeneral.com' in url_lower:
        return 'AmGeneral'
    elif 'takaful-ikhlas.com' in url_lower:
        return 'Takaful Ikhlas'
    elif 'berjayasompo.com' in url_lower:
        return 'Berjaya Sompo'
    elif 'tokiomarine.com' in url_lower:
        return 'Tokio Marine'
    elif 'greateastern.com' in url_lower:
        return 'Great Eastern General'
    else:
        return 'Unknown Insurer'

async def store_policies_background(policies: List):
    """Background task to store policies in database"""
    try:
        stored_count = 0
        for policy in policies:
            policy_id = await policy_ops.insert_policy(policy)
            if policy_id:
                stored_count += 1
        
        logger.info(f"Background storage completed: {stored_count}/{len(policies)} policies stored")
        
    except Exception as e:
        logger.error(f"Error in background policy storage: {e}")
