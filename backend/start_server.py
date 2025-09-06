#!/usr/bin/env python3
"""
Simple startup script for the InsureWiz FastAPI server with auto-reload
"""

import uvicorn
from main import app

if __name__ == "__main__":
    print("🚀 Starting InsureWiz AI Chatbot API server with auto-reload...")
    print("📍 Server will be available at: http://localhost:8000")
    print("📖 API documentation at: http://localhost:8000/docs")
    print("🔍 Health check at: http://localhost:8000/health")
    print("🔄 Auto-reload enabled - server will restart on file changes")
    print("\nPress Ctrl+C to stop the server")
    print("-" * 50)
    
    uvicorn.run(
        "main:app", 
        host="0.0.0.0", 
        port=8000,
        log_level="info",
        reload=True,
        reload_dirs=["app", "."],  # Watch app directory and current directory
        reload_excludes=["*.pyc", "__pycache__", "*.log", "*.tmp"]
    )

