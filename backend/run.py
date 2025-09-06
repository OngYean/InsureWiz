#!/usr/bin/env python3
"""
Main entry point for the InsureWiz FastAPI server with auto-reload
"""

import uvicorn
from app.dynamic_app import app

if __name__ == "__main__":
    print("🚀 Starting InsureWiz AI Chatbot API server with auto-reload...")
    print("🚀 Starting InsureWiz Dynamic Insurance Comparator...")
    print("📊 Features: Real-time scraping + AI analysis")
    print("📍 Server will be available at: http://localhost:8000")
    print("📖 API documentation at: http://localhost:8000/docs")
    print("🔍 Health check at: http://localhost:8000/health")
    print("🔍 Dynamic scraping at: http://localhost:8000/dynamic/")
    print("🤖 AI analysis at: http://localhost:8000/advanced/")
    print("\nPress Ctrl+C to stop the server")
    print("-" * 50)
    
    uvicorn.run(
        "main:app", 
        host="0.0.0.0", 
        port=8000,
        log_level="info",
        reload=False,
        reload_dirs=["app", "."],  # Watch app directory and current directory
        reload_excludes=["*.pyc", "__pycache__", "*.log", "*.tmp"]
    )

