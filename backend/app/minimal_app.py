"""
Minimal FastAPI app for testing the insurance comparator
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Insurance Comparator API",
    description="Simple API for comparing Malaysian motor insurance policies",
    version="1.0.0"
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
    logger.info("Simple router included successfully")
except Exception as e:
    logger.error(f"Failed to include simple router: {e}")

try:
    from app.comparator.api.advanced import router as advanced_router
    app.include_router(advanced_router)
    logger.info("Advanced router included successfully")
except Exception as e:
    logger.error(f"Failed to include advanced router: {e}")

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Insurance Comparator API",
        "status": "running",
        "endpoints": {
            "basic": [
                "/simple/health",
                "/simple/policies", 
                "/simple/insurers",
                "/simple/compare",
                "/simple/stats"
            ],
            "advanced": [
                "/advanced/health",
                "/advanced/compare",
                "/advanced/features",
                "/advanced/comparison/{session_id}"
            ],
            "documentation": [
                "/docs",
                "/redoc"
            ]
        }
    }

@app.get("/health")
async def health():
    """Health check endpoint"""
    return {"status": "healthy", "service": "insurance_comparator"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
