from fastapi import APIRouter, HTTPException, Depends
from app.models.chat import ChatRequest, ChatResponse
from app.services.ai_service import ai_service
from app.utils.logger import setup_logger

logger = setup_logger("chat_api")

router = APIRouter(prefix="/api/chat", tags=["chat"])

@router.post("/", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Generate AI response for insurance-related questions
    
    Args:
        request: Chat request containing user message and optional session ID
        
    Returns:
        ChatResponse: AI-generated response with timestamp
        
    Raises:
        HTTPException: If there's an error processing the request
    """
    try:
        logger.info(f"Processing chat request: {request.message[:50]}...")
        
        # Generate AI response
        ai_response = await ai_service.generate_response(request.message)
        
        # Create response
        response = ChatResponse(
            response=ai_response,
            session_id=request.session_id
        )
        
        logger.info("Chat request processed successfully")
        return response
        
    except Exception as e:
        logger.error(f"Error processing chat request: {str(e)}")
        raise HTTPException(
            status_code=500, 
            detail=f"Error processing chat request: {str(e)}"
        )

@router.get("/health")
async def chat_health():
    """Health check endpoint for chat service"""
    return {"status": "healthy", "service": "Chat AI Service"}
