"""
InsureWiz AI Chatbot API - Main Entry Point

This is the main entry point for the FastAPI application.
The actual application logic is organized in the app/ package.
"""

import uvicorn
from app.core.app import app
from app.config import settings

if __name__ == "__main__":
    uvicorn.run(
        "app.core.app:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
        log_level="info"
    )
