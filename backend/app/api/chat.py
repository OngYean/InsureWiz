from fastapi import APIRouter, HTTPException, Depends
from app.models.chat import ChatRequest, ChatResponse, RAGChatRequest, RAGChatResponse
from app.services.ai_service import ai_service
from app.services.document_service import document_service
from app.utils.logger import setup_logger
from typing import Dict, Any

logger = setup_logger("chat_api")

router = APIRouter(prefix="/api/chat", tags=["chat"])

@router.post("/", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Generate AI response for insurance-related questions (basic mode)
    
    Args:
        request: Chat request containing user message and optional session ID
        
    Returns:
        ChatResponse: AI-generated response with timestamp
        
    Raises:
        HTTPException: If there's an error processing the request
    """
    try:
        logger.info(f"Processing basic chat request: {request.message[:50]}...")
        
        # Generate AI response
        ai_response = await ai_service.generate_response(request.message)
        
        # Create response
        response = ChatResponse(
            response=ai_response,
            session_id=request.session_id
        )
        
        logger.info("Basic chat request processed successfully")
        return response
        
    except Exception as e:
        logger.error(f"Error processing basic chat request: {str(e)}")
        raise HTTPException(
            status_code=500, 
            detail=f"Error processing chat request: {str(e)}"
        )

@router.post("/rag", response_model=RAGChatResponse)
async def chat_with_rag(request: RAGChatRequest):
    """
    Generate AI response using RAG with knowledge base retrieval
    
    Args:
        request: RAG chat request containing user message and optional session ID
        
    Returns:
        RAGChatResponse: AI-generated response with sources and RAG metadata
        
    Raises:
        HTTPException: If there's an error processing the request
    """
    try:
        logger.info(f"Processing RAG chat request: {request.message[:50]}...")
        
        # Generate RAG response
        rag_response = await ai_service.generate_rag_response(
            request.message, 
            namespace=request.namespace or "insurance_knowledge"
        )
        
        # Create RAG response
        response = RAGChatResponse(
            response=rag_response["response"],
            session_id=request.session_id,
            sources=rag_response.get("sources", []),
            rag_used=rag_response.get("rag_used", False),
            context_docs=rag_response.get("context_docs", 0)
        )
        
        logger.info("RAG chat request processed successfully")
        return response
        
    except Exception as e:
        logger.error(f"Error processing RAG chat request: {str(e)}")
        raise HTTPException(
            status_code=500, 
            detail=f"Error processing RAG chat request: {str(e)}"
        )

@router.post("/initialize-knowledge")
async def initialize_knowledge_base():
    """
    Initialize the knowledge base with default insurance information
    
    Returns:
        Dict: Status of knowledge base initialization
        
    Raises:
        HTTPException: If there's an error initializing the knowledge base
    """
    try:
        logger.info("Initializing insurance knowledge base...")
        
        success = await ai_service.initialize_knowledge_base()
        
        if success:
            logger.info("Insurance knowledge base initialized successfully")
            return {
                "status": "success",
                "message": "Insurance knowledge base initialized successfully",
                "timestamp": "now"
            }
        else:
            logger.error("Failed to initialize insurance knowledge base")
            raise HTTPException(
                status_code=500,
                detail="Failed to initialize insurance knowledge base"
            )
            
    except Exception as e:
        logger.error(f"Error initializing insurance knowledge base: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error initializing insurance knowledge base: {str(e)}"
        )

@router.post("/initialize-project-knowledge")
async def initialize_project_knowledge_base():
    """
    Initialize the project knowledge base with project documentation
    
    Returns:
        Dict: Status of project knowledge base initialization
        
    Raises:
        HTTPException: If there's an error initializing the project knowledge base
    """
    try:
        logger.info("Initializing project knowledge base...")
        
        success = await ai_service.initialize_project_knowledge_base()
        
        if success:
            logger.info("Project knowledge base initialized successfully")
            return {
                "status": "success",
                "message": "Project knowledge base initialized successfully",
                "timestamp": "now"
            }
        else:
            logger.error("Failed to initialize project knowledge base")
            raise HTTPException(
                status_code=500,
                detail="Failed to initialize project knowledge base"
            )
            
    except Exception as e:
        logger.error(f"Error initializing project knowledge base: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error initializing project knowledge base: {str(e)}"
        )

@router.post("/initialize-all-knowledge")
async def initialize_all_knowledge_bases():
    """
    Initialize both insurance and project knowledge bases
    
    Returns:
        Dict: Status of all knowledge base initialization
        
    Raises:
        HTTPException: If there's an error initializing the knowledge bases
    """
    try:
        logger.info("Initializing all knowledge bases...")
        
        success = await ai_service.initialize_all_knowledge_bases()
        
        if success:
            logger.info("All knowledge bases initialized successfully")
            return {
                "status": "success",
                "message": "All knowledge bases initialized successfully",
                "timestamp": "now"
            }
        else:
            logger.error("Failed to initialize all knowledge bases")
            raise HTTPException(
                status_code=500,
                detail="Failed to initialize all knowledge bases"
            )
            
    except Exception as e:
        logger.error(f"Error initializing all knowledge bases: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error initializing all knowledge bases: {str(e)}"
        )

@router.get("/knowledge-stats")
async def get_knowledge_stats():
    """
    Get statistics about the knowledge base
    
    Returns:
        Dict: Knowledge base statistics
        
    Raises:
        HTTPException: If there's an error retrieving statistics
    """
    try:
        logger.info("Retrieving knowledge base statistics...")
        
        stats = document_service.get_knowledge_stats()
        
        logger.info("Knowledge base statistics retrieved successfully")
        return {
            "status": "success",
            "stats": stats,
            "timestamp": "now"
        }
        
    except Exception as e:
        logger.error(f"Error retrieving knowledge base statistics: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving knowledge base statistics: {str(e)}"
        )

@router.get("/project-knowledge-stats")
async def get_project_knowledge_stats():
    """
    Get statistics about the project knowledge base
    
    Returns:
        Dict: Project knowledge base statistics
        
    Raises:
        HTTPException: If there's an error retrieving project knowledge statistics
    """
    try:
        logger.info("Retrieving project knowledge base statistics...")
        
        from app.services.project_document_service import project_document_service
        stats = project_document_service.get_project_docs_stats()
        
        logger.info("Project knowledge base statistics retrieved successfully")
        return {
            "status": "success",
            "stats": stats,
            "timestamp": "now"
        }
        
    except Exception as e:
        logger.error(f"Error retrieving project knowledge base statistics: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving project knowledge base statistics: {str(e)}"
        )

@router.get("/health")
async def chat_health():
    """Health check endpoint for chat service"""
    return {"status": "healthy", "service": "Chat AI Service with RAG"}

@router.get("/rag-status")
async def rag_status():
    """Check RAG system status"""
    try:
        # Check if RAG chain is available
        rag_available = ai_service.rag_chain is not None
        
        # Check vector store status
        try:
            stats = document_service.get_knowledge_stats()
            vector_store_healthy = True
        except:
            vector_store_healthy = False
        
        # Check project knowledge base status
        try:
            from app.services.project_document_service import project_document_service
            project_stats = project_document_service.get_project_docs_stats()
            project_knowledge_healthy = True
        except:
            project_knowledge_healthy = False
        
        return {
            "status": "healthy",
            "rag_available": rag_available,
            "vector_store_healthy": vector_store_healthy,
            "project_knowledge_healthy": project_knowledge_healthy,
            "service": "RAG System Status",
            "knowledge_bases": {
                "insurance": vector_store_healthy,
                "project": project_knowledge_healthy
            }
        }
        
    except Exception as e:
        return {
            "status": "unhealthy",
            "rag_available": False,
            "vector_store_healthy": False,
            "project_knowledge_healthy": False,
            "error": str(e),
            "service": "RAG System Status"
        }
