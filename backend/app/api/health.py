from fastapi import APIRouter

router = APIRouter(tags=["health"])

@router.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "InsureWiz AI Chatbot API is running!",
        "version": "1.0.0",
        "status": "active"
    }

@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "InsureWiz AI Chatbot",
        "timestamp": "2024-01-01T00:00:00Z"
    }

@router.get("/info")
async def api_info():
    """API information endpoint"""
    return {
        "name": "InsureWiz AI Chatbot API",
        "version": "1.0.0",
        "description": "AI-powered insurance advisor chatbot API",
        "endpoints": {
            "chat": "/api/chat",
            "health": "/health",
            "docs": "/docs"
        }
    }

