#!/usr/bin/env python3
"""
Main entry point for the InsureWiz Dynamic Insurance Comparator
"""

import uvicorn
from app.dynamic_app import app

if __name__ == "__main__":
    print("🚀 Starting InsureWiz Dynamic Insurance Comparator...")
    print("📊 Features: Real-time scraping + AI analysis")
    print("📍 Server will be available at: http://localhost:8000")
    print("📖 API documentation at: http://localhost:8000/docs")
    print("🔍 Dynamic scraping at: http://localhost:8000/dynamic/")
    print("🤖 AI analysis at: http://localhost:8000/advanced/")
    print("\nPress Ctrl+C to stop the server")
    print("-" * 50)
    
    uvicorn.run(
        app, 
        host="0.0.0.0", 
        port=8000,
        reload=False
    )

