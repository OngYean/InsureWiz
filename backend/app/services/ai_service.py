from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import HumanMessage, SystemMessage
from typing import List
from app.config import settings
from app.utils.logger import setup_logger
from app.utils.exceptions import AIServiceException

logger = setup_logger("ai_service")

class AIService:
    """Service for AI-related operations"""
    
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(
            model=settings.ai_model,
            temperature=settings.ai_temperature,
            google_api_key=settings.google_api_key,
            convert_system_message_to_human=True
        )
        
        # Insurance-specific system prompt
        self.insurance_system_prompt = """You are an expert AI Insurance Advisor with deep knowledge of insurance policies, coverage types, claims processes, and risk management. Your role is to:

1. Provide accurate, helpful information about insurance concepts
2. Explain complex insurance terms in simple, understandable language
3. Offer general guidance on insurance decisions (but not specific financial advice)
4. Help users understand their coverage options and policy details
5. Guide users through claims processes and requirements
6. Explain factors that affect insurance premiums and costs

Key areas of expertise:
- Auto insurance (liability, collision, comprehensive, uninsured motorist)
- Home insurance (property, liability, additional coverages)
- Health insurance (plans, deductibles, copays, networks)
- Life insurance (term, whole, universal, riders)
- Business insurance (general liability, professional liability, workers comp)
- Claims processes and documentation requirements
- Risk assessment and mitigation strategies

IMPORTANT: Always remind users that your advice is for informational purposes only and they should consult with licensed insurance professionals for specific advice about their policies and coverage needs.

Be conversational, empathetic, and professional. Use examples when helpful to illustrate concepts."""
    
    async def generate_response(self, user_message: str) -> str:
        """Generate AI response for user message"""
        try:
            # Create messages for the conversation
            messages = [
                SystemMessage(content=self.insurance_system_prompt),
                HumanMessage(content=user_message)
            ]
            
            # Get AI response
            response = self.llm.invoke(messages)
            
            logger.info(f"AI response generated successfully for message: {user_message[:50]}...")
            return response.content
            
        except Exception as e:
            logger.error(f"Error generating AI response: {str(e)}")
            raise AIServiceException(
                message="Failed to generate AI response",
                details={"error": str(e), "user_message": user_message[:100]}
            )
    
    async def generate_response_with_context(self, user_message: str, conversation_history: List[dict]) -> str:
        """Generate AI response with conversation context"""
        try:
            # Build messages with conversation history
            messages = [SystemMessage(content=self.insurance_system_prompt)]
            
            # Add conversation history
            for msg in conversation_history[-5:]:  # Last 5 messages for context
                if msg.get('role') == 'user':
                    messages.append(HumanMessage(content=msg.get('content', '')))
                elif msg.get('role') == 'assistant':
                    messages.append(SystemMessage(content=msg.get('content', '')))
            
            # Add current user message
            messages.append(HumanMessage(content=user_message))
            
            # Get AI response
            response = self.llm.invoke(messages)
            
            logger.info(f"AI response generated with context for message: {user_message[:50]}...")
            return response.content
            
        except Exception as e:
            logger.error(f"Error generating AI response with context: {str(e)}")
            raise AIServiceException(
                message="Failed to generate AI response with context",
                details={"error": str(e), "user_message": user_message[:100]}
            )

# Global AI service instance
ai_service = AIService()
