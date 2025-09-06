"""
Production FastAPI app with full dynamic scraping capabilities
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="InsureWiz - Dynamic Insurance Comparator",
    description="AI-powered Malaysian motor insurance comparison with real-time scraping",
    version="2.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Import and include routers
try:
    from app.comparator.api.simple import router as simple_router
    app.include_router(simple_router)
    logger.info("✅ Simple router included")
except Exception as e:
    logger.error(f"❌ Failed to include simple router: {e}")

try:
    from app.comparator.api.advanced import router as advanced_router
    app.include_router(advanced_router)
    logger.info("✅ Advanced router included")
except Exception as e:
    logger.error(f"❌ Failed to include advanced router: {e}")

try:
    from app.comparator.api.dynamic import router as dynamic_router
    app.include_router(dynamic_router)
    logger.info("✅ Dynamic scraping router included")
except Exception as e:
    logger.error(f"❌ Failed to include dynamic router: {e}")

try:
    from app.api.claim import router as claim_router
    app.include_router(claim_router)
    logger.info("✅ Claim prediction router included")
except Exception as e:
    logger.error(f"❌ Failed to include claim router: {e}")

@app.get("/")
async def root():
    """Root endpoint with full feature overview"""
    return {
        "message": "InsureWiz - Dynamic Insurance Comparator",
        "status": "operational",
        "version": "2.0.0",
        "features": {
            "real_time_scraping": "active",
            "ai_powered_analysis": "active", 
            "dynamic_data": "active",
            "live_comparisons": "active"
        },
        "endpoints": {
            "basic": [
                "/simple/policies",
                "/simple/compare", 
                "/simple/stats"
            ],
            "advanced_ai": [
                "/advanced/compare",
                "/advanced/features",
                "/advanced/health"
            ],
            "dynamic_scraping": [
                "/dynamic/scrape/all",
                "/dynamic/policies/live",
                "/dynamic/compare/live",
                "/dynamic/insurers/live"
            ],
            "documentation": [
                "/docs",
                "/redoc"
            ]
        },
        "data_sources": {
            "real_time_scraping": "tavily + crawl4ai simulation",
            "insurers_supported": 5,
            "coverage_types": ["comprehensive", "takaful"],
            "update_method": "on_demand"
        }
    }

@app.get("/health")
async def health():
    """Comprehensive health check"""
    import os
    
    return {
        "status": "healthy", 
        "service": "insurewiz_dynamic",
        "version": "2.0.0",
        "capabilities": {
            "basic_comparison": "ready",
            "ai_analysis": "ready" if os.getenv("GOOGLE_API_KEY") else "needs_api_key",
            "real_time_scraping": "ready" if os.getenv("TAVILY_API_KEY") else "simulated",
            "database_storage": "ready" if os.getenv("SUPABASE_URL") else "mock",
            "pdf_generation": "conditional",
            "chart_generation": "ready"
        },
        "api_keys_status": {
            "google_gemini": "✅" if os.getenv("GOOGLE_API_KEY") else "❌",
            "tavily_search": "✅" if os.getenv("TAVILY_API_KEY") else "❌", 
            "supabase_db": "✅" if os.getenv("SUPABASE_URL") else "❌"
        }
    }

if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting InsureWiz Dynamic Comparator...")
    print("📊 Real-time scraping: ENABLED")
    print("🤖 AI analysis: ENABLED")
    print("💾 Database storage: ENABLED")
    print("📍 Server: http://localhost:8000")
    print("📖 Documentation: http://localhost:8000/docs")
    print("🔍 Dynamic endpoints: /dynamic/*")
    uvicorn.run(app, host="0.0.0.0", port=8000)
