from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.services.validator.api_endpoints import router as validator_router
from app.api import chat, health, claim
from app.comparator.api import comparator_router
from app.comparator.api.dynamic import router as dynamic_router
from app.utils.logger import setup_logger
from app.utils.exceptions import handle_insurewiz_exception, InsureWizException
from app.middleware.logging import LoggingMiddleware
from app.core.startup import create_startup_event

# Configure logging
logger = setup_logger("insurewiz")

def create_app() -> FastAPI:
    """Create and configure FastAPI application"""
    
    app = FastAPI(
        title=settings.api_title,
        version=settings.api_version,
        description=settings.api_description,
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json"
    )
    
    # Add custom middleware
    app.add_middleware(LoggingMiddleware)
    
    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.allowed_origins,
        allow_credentials=settings.cors_allow_credentials,
        allow_methods=settings.cors_allow_methods,
        allow_headers=settings.cors_allow_headers,
    )
    
    # Include routers
    app.include_router(health.router)
    app.include_router(chat.router)
    app.include_router(validator_router)
    app.include_router(claim.router, tags=["Advanced Claims"])  # Remove extra prefix, claim router already has /advanced
    app.include_router(comparator_router)
    app.include_router(dynamic_router)  # Add dynamic router for /dynamic/compare/live endpoint
    
    # Add exception handler for custom exceptions
    @app.exception_handler(InsureWizException)
    async def insurewiz_exception_handler(request, exc: InsureWizException):
        return handle_insurewiz_exception(exc)
    
    # Add startup event
    @app.on_event("startup")
    async def startup_event():
        logger.info("Starting InsureWiz AI Chatbot API...")
        logger.info(f"API Title: {settings.api_title}")
        logger.info(f"API Version: {settings.api_version}")
        logger.info(f"Debug Mode: {settings.debug}")
    
    # Add shutdown event
    @app.on_event("shutdown")
    async def shutdown_event():
        logger.info("Shutting down InsureWiz AI Chatbot API...")
    
    # Initialize RAG and knowledge base services
    create_startup_event(app)
    
    return app

# Create app instance
app = create_app()
