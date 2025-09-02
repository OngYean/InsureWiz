from pydantic_settings import BaseSettings
from typing import List
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Settings(BaseSettings):
    """Application settings and configuration"""
    
    # API Configuration
    api_title: str = "InsureWiz AI Chatbot API"
    api_version: str = "1.0.0"
    api_description: str = "AI-powered insurance advisor chatbot API"
    
    # Server Configuration
    host: str = "0.0.0.0"
    port: int = 8000
    debug: bool = False
    
    # CORS Configuration
    allowed_origins: List[str] = [
        "http://localhost:3000",
        "http://127.0.0.1:3000"
    ]
    
    # AI Configuration
    google_api_key: str = os.getenv("GOOGLE_API_KEY", "")
    ai_model: str = "gemini-2.0-flash"
    ai_temperature: float = 0.7
    
    # Pinecone Configuration
    pinecone_api_key: str = os.getenv("PINECONE_API_KEY", "")
    pinecone_environment: str = os.getenv("PINECONE_ENVIRONMENT", "gcp-starter")
    pinecone_index_name: str = os.getenv("PINECONE_INDEX_NAME", "insurewiz")
    
    # RAG Configuration
    chunk_size: int = 1000
    chunk_overlap: int = 200
    top_k_results: int = 5
    
    # Security
    cors_allow_credentials: bool = True
    cors_allow_methods: List[str] = ["*"]
    cors_allow_headers: List[str] = ["*"]
    
    class Config:
        env_file = ".env"
        case_sensitive = False
        extra = "ignore"  # Ignore extra fields from environment

# Global settings instance
settings = Settings()

# Validate required settings
if not settings.google_api_key:
    raise ValueError("GOOGLE_API_KEY environment variable is required")

if not settings.pinecone_api_key:
    raise ValueError("PINECONE_API_KEY environment variable is required")

