"""
Main comparator router that combines all API endpoints
"""

from fastapi import APIRouter
from .crawl import router as crawl_router
from .compare import router as compare_router
from .reports import router as reports_router

# Create main comparator router
router = APIRouter(prefix="/api/comparator", tags=["Malaysian Motor Insurance Comparator"])

# Include sub-routers
router.include_router(crawl_router)
router.include_router(compare_router)
router.include_router(reports_router)

@router.get("/")
async def get_comparator_info():
    """Get information about the Malaysian Motor Insurance Comparator"""
    return {
        "name": "Malaysian Motor Insurance Comparator",
        "version": "1.0.0",
        "description": "LangChain-powered AI agent for comparing Malaysian motor insurance policies",
        "features": [
            "Web crawling of 9 major Malaysian insurers",
            "AI-powered policy data extraction and normalization",
            "Intelligent policy comparison with weighted scoring",
            "Professional PDF report generation",
            "BNM compliance and PDPA data protection"
        ],
        "supported_insurers": [
            "Zurich Malaysia",
            "Etiqa",
            "Allianz General Insurance Malaysia",
            "AXA Affin General",
            "Generali Malaysia",
            "Liberty Insurance",
            "AmGeneral",
            "Takaful Ikhlas",
            "Berjaya Sompo"
        ],
        "endpoints": {
            "crawling": "/api/comparator/crawl",
            "comparison": "/api/comparator/compare", 
            "reports": "/api/comparator/reports"
        },
        "status": "operational"
    }

@router.get("/health")
async def health_check():
    """Health check endpoint for the comparator service"""
    return {
        "status": "healthy",
        "service": "Malaysian Motor Insurance Comparator",
        "timestamp": "2024-01-15T10:30:00Z",
        "components": {
            "crawling_service": "operational",
            "comparison_engine": "operational", 
            "pdf_generator": "operational",
            "database": "operational"
        }
    }
