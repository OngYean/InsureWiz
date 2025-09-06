from fastapi import FastAPI
from app.services.ai_service import ai_service
from app.utils.logger import setup_logger
import asyncio

logger = setup_logger("startup")

async def initialize_services(app: FastAPI):
    """Initialize all services on startup"""
    try:
        logger.info("Starting service initialization...")
        
        # Initialize knowledge base
        logger.info("Initializing knowledge base...")
        kb_success = await ai_service.initialize_knowledge_base()
        
        if kb_success:
            logger.info("✅ Knowledge base initialized successfully")
        else:
            logger.warning("⚠️ Knowledge base initialization failed, continuing without RAG")
        
        # Check RAG system status
        try:
            # Test RAG functionality by checking if we can generate a basic response
            test_response = await ai_service.generate_rag_response("test")
            if test_response:
                logger.info("✅ RAG system initialized successfully")
            else:
                logger.warning("⚠️ RAG system not available, using basic AI responses")
        except Exception as e:
            logger.warning(f"⚠️ RAG system check failed: {str(e)}, using basic AI responses")
        
        logger.info("Service initialization completed")
        
    except Exception as e:
        logger.error(f"Error during service initialization: {str(e)}")
        logger.warning("Continuing with basic functionality")

def create_startup_event(app: FastAPI):
    """Create startup event for FastAPI app"""
    @app.on_event("startup")
    async def startup_event():
        await initialize_services(app)

