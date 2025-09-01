#!/usr/bin/env python3
"""
Main entry point for the InsureWiz FastAPI server
"""

import uvicorn
from main import app

if __name__ == "__main__":
    print("🚀 Starting InsureWiz AI Chatbot API server...")
    print("📍 Server will be available at: http://localhost:8000")
    print("📖 API documentation at: http://localhost:8000/docs")
    print("🔍 Health check at: http://localhost:8000/health")
    print("\nPress Ctrl+C to stop the server")
    print("-" * 50)
    
    uvicorn.run(
        app, 
        host="0.0.0.0", 
        port=8000,
        log_level="info"
    )

