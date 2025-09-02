from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import HumanMessage, SystemMessage
from langchain.memory import ConversationBufferMemory
from typing import List, Dict, Any
from app.config import settings
from app.services.vector_store import vector_store_service
from app.services.document_service import document_service
from app.services.project_document_service import project_document_service
from app.utils.logger import setup_logger
from app.utils.exceptions import AIServiceException, VectorStoreException

logger = setup_logger("ai_service")

class AIService:
    """Service for AI-related operations with RAG integration"""
    
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(
            model=settings.ai_model,
            temperature=settings.ai_temperature,
            google_api_key=settings.google_api_key
        )
        
        # Initialize conversation memory
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True
        )
        
        # Simplified RAG approach - no complex chain initialization
        logger.info("AI service initialized with simplified RAG approach")
        
        # Malaysian Insurance & Takaful system prompt
        self.insurance_system_prompt = """You are an Expert AI Insurance Advisor specialized in Malaysian insurance and Takaful policies. You have deep knowledge of insurance coverage types, claims processes, and risk management practices relevant to Malaysia.

Your role is to:

1. Provide accurate and helpful information about Malaysian insurance concepts.
2. Explain complex insurance terms in simple, understandable language, using local examples when possible.
3. Offer general guidance on insurance and Takaful decisions (but never specific financial advice).
4. Help users understand their coverage options and policy details, including common Malaysian exclusions and riders.
5. Guide users through claims processes and documentation requirements in Malaysia (e.g., JPJ/PDRM reports for motor claims, Bank Negara guidelines for disputes).
6. Explain factors affecting insurance premiums in Malaysia, such as No Claim Discount (NCD), sum insured, driver's age, flood coverage, and location-based risks.

Key Areas of Expertise in Malaysia:

Motor/Auto Insurance & Takaful:
- Third-party, comprehensive, windscreen, special perils coverage
- No Claim Discount (NCD) system and calculations
- JPJ/PDRM requirements for claims
- Flood coverage under special perils
- Malaysian road conditions and risk factors

Home/Property Insurance & Takaful:
- Fire, contents, liability coverage
- Mortgage protection (MRTA/MLTA)
- Flood and natural disaster coverage
- Malaysian property market considerations
- Location-based risk assessments

Health Insurance & Medical Takaful:
- Hospitalisation coverage and panel hospitals
- Critical illness protection
- Deductibles, co-pays, and waiting periods
- Malaysian healthcare system integration
- Pre-existing condition considerations

Life Insurance & Family Takaful:
- Term, whole life, investment-linked products
- Riders and additional benefits
- MRTA/MLTA for property financing
- Malaysian family protection needs
- Investment and savings components

Business Insurance:
- General liability and professional indemnity
- Workers' compensation requirements
- SME packages and business interruption
- Malaysian business regulations
- Industry-specific coverage needs

Claims Processes:
- Reporting timelines and procedures
- Required documentation (JPJ reports, medical certificates)
- Repair approvals and network workshops
- Hospital claims and panel hospital benefits
- Dispute resolution through Bank Negara

Risk Management:
- Personal and business risk reduction strategies
- Malaysian context considerations
- Natural disaster preparedness
- Financial planning integration

Language Support:
- Support Malay (Bahasa Malaysia), English, and Chinese (Simplified or Traditional)
- Always respond in the language of the user's query
- If unclear, politely ask which language they prefer

Tone & Style:
- Be conversational, empathetic, and professional
- Use Malaysian context and examples (flood coverage, NCD, panel hospitals)
- Explain concepts with local relevance
- Provide practical, actionable guidance

⚠️ IMPORTANT DISCLAIMER: This information is for general purposes only. Please consult a licensed insurance or Takaful professional in Malaysia for advice specific to your policy and coverage needs.

Always include this disclaimer at the end of your responses."""
    
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
    
    async def generate_rag_response(self, user_message: str, namespace: str = None) -> Dict[str, Any]:
        """Generate AI response using RAG with intelligent knowledge base selection"""
        try:
            # Determine which knowledge base to use based on the query
            knowledge_type, relevant_docs = self._determine_knowledge_base(user_message)
            
            if not relevant_docs:
                # Fallback to basic response if no relevant documents found
                logger.warning("No relevant documents found, falling back to basic response")
                basic_response = await self.generate_response(user_message)
                return {
                    "response": basic_response,
                    "sources": [],
                    "rag_used": False,
                    "knowledge_type": "none"
                }
            
            # Create enhanced prompt based on knowledge type
            if knowledge_type == "project":
                enhanced_prompt = self._create_project_prompt(user_message, relevant_docs)
            else:
                enhanced_prompt = self._create_insurance_prompt(user_message, relevant_docs)
            
            # Generate response with enhanced prompt
            messages = [
                SystemMessage(content=enhanced_prompt),
                HumanMessage(content=user_message)
            ]
            
            response = self.llm.invoke(messages)
            
            # Format source information
            sources = self._format_sources(relevant_docs)
            
            logger.info(f"RAG response generated successfully for message: {user_message[:50]}...")
            
            return {
                "response": response.content,
                "sources": sources,
                "rag_used": True,
                "knowledge_type": knowledge_type,
                "context_docs": len(relevant_docs)
            }
            
        except Exception as e:
            logger.error(f"Error generating RAG response: {str(e)}")
            # Fallback to basic response
            try:
                basic_response = await self.generate_response(user_message)
                return {
                    "response": basic_response,
                    "sources": [],
                    "rag_used": False,
                    "error": str(e),
                    "knowledge_type": "none"
                }
            except Exception as fallback_error:
                raise AIServiceException(
                    message="Failed to generate RAG response and fallback",
                    details={"error": str(e), "fallback_error": str(fallback_error), "user_message": user_message[:100]}
                )
    
    def _determine_knowledge_base(self, user_message: str) -> tuple[str, List]:
        """Intelligently determine which knowledge base to search based on user query"""
        try:
            # Keywords that indicate project-related questions
            project_keywords = [
                "project", "code", "architecture", "setup", "installation", "development",
                "backend", "frontend", "api", "database", "deployment", "configuration",
                "structure", "files", "modules", "services", "endpoints", "routes",
                "models", "schemas", "middleware", "authentication", "security",
                "testing", "documentation", "readme", "guide", "tutorial"
            ]
            
            # Keywords that indicate insurance-related questions
            insurance_keywords = [
                "insurance", "takaful", "policy", "coverage", "claim", "premium",
                "motor", "auto", "car", "home", "property", "health", "medical",
                "life", "family", "business", "liability", "risk", "malaysia",
                "malaysian", "ncd", "jpj", "pdrm", "bank negara", "flood"
            ]
            
            # Count keyword matches
            user_message_lower = user_message.lower()
            project_score = sum(1 for keyword in project_keywords if keyword in user_message_lower)
            insurance_score = sum(1 for keyword in insurance_keywords if keyword in user_message_lower)
            
            logger.info(f"Knowledge base scores - Project: {project_score}, Insurance: {insurance_score}")
            
            # Determine which knowledge base to search
            if project_score > insurance_score:
                logger.info("Using project knowledge base")
                relevant_docs = project_document_service.search_project_knowledge(user_message)
                return "project", relevant_docs
            elif insurance_score > 0:
                logger.info("Using insurance knowledge base")
                relevant_docs = document_service.search_knowledge(user_message)
                return "insurance", relevant_docs
            else:
                logger.info("No clear knowledge base preference, trying both")
                # Try project knowledge first, then insurance
                project_docs = project_document_service.search_project_knowledge(user_message)
                if project_docs:
                    return "project", project_docs
                
                insurance_docs = document_service.search_knowledge(user_message)
                if insurance_docs:
                    return "insurance", insurance_docs
                
                return "none", []
                
        except Exception as e:
            logger.error(f"Error determining knowledge base: {str(e)}")
            return "none", []
    
    def _create_project_prompt(self, user_message: str, relevant_docs: List) -> str:
        """Create enhanced prompt for project-related questions"""
        context = self._format_context(relevant_docs)
        
        return f"""You are an AI assistant specialized in helping users understand the InsureWiz project. You have access to the project's documentation and can provide detailed information about the project structure, architecture, setup, and development.

Project Context:
{context}

User Question: {user_message}

Please provide a comprehensive answer based on the project documentation above. Focus on:
1. Explaining the project structure and components
2. Describing how different parts work together
3. Providing setup and development guidance
4. Explaining the technical architecture and design decisions
5. Offering practical advice for development and deployment

If the documentation doesn't contain specific information about the user's question, use your general knowledge but clearly indicate when you're providing information from your training data versus the project documentation.

Always be helpful, clear, and provide actionable information when possible."""
    
    def _create_insurance_prompt(self, user_message: str, relevant_docs: List) -> str:
        """Create enhanced prompt for insurance-related questions"""
        context = self._format_context(relevant_docs)
        
        return f"""{self.insurance_system_prompt}

Relevant Information from Knowledge Base:
{context}

User Question: {user_message}

Please provide a comprehensive answer based on the knowledge base information above, combined with your expertise in Malaysian insurance and Takaful. If the knowledge base doesn't contain specific information about the user's question, use your general knowledge but clearly indicate when you're providing information from your training data versus the knowledge base."""
    
    def _format_context(self, documents: List) -> str:
        """Format retrieved documents into context string"""
        if not documents:
            return "No specific information found in knowledge base for this query."
        
        context_parts = []
        for i, doc in enumerate(documents, 1):
            source = doc.metadata.get('source', 'Unknown')
            category = doc.metadata.get('category', 'General')
            content = doc.page_content.strip()
            
            context_parts.append(f"""
            Source {i}: {source} ({category})
            Content: {content}
            """)
        
        return "\n".join(context_parts)
    
    def _format_sources(self, documents: List) -> List[Dict[str, str]]:
        """Format source documents for response"""
        sources = []
        for doc in documents:
            sources.append({
                "source": doc.metadata.get('source', 'Unknown'),
                "category": doc.metadata.get('category', 'General'),
                "content_preview": doc.page_content[:200] + "..." if len(doc.page_content) > 200 else doc.page_content
            })
        return sources
    
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
    
    async def initialize_knowledge_base(self) -> bool:
        """Initialize the knowledge base with default insurance information"""
        try:
            success = document_service.add_insurance_knowledge()
            if success:
                logger.info("Insurance knowledge base initialized successfully")
                return True
            else:
                logger.error("Failed to initialize insurance knowledge base")
                return False
                
        except Exception as e:
            logger.error(f"Error initializing insurance knowledge base: {str(e)}")
            return False
    
    async def initialize_project_knowledge_base(self) -> bool:
        """Initialize the project knowledge base with project documentation"""
        try:
            success = project_document_service.ingest_project_documentation()
            if success:
                logger.info("Project knowledge base initialized successfully")
                return True
            else:
                logger.error("Failed to initialize project knowledge base")
                return False
                
        except Exception as e:
            logger.error(f"Error initializing project knowledge base: {str(e)}")
            return False
    
    async def initialize_all_knowledge_bases(self) -> bool:
        """Initialize both insurance and project knowledge bases"""
        try:
            logger.info("Initializing all knowledge bases...")
            
            # Initialize insurance knowledge base
            insurance_success = await self.initialize_knowledge_base()
            
            # Initialize project knowledge base
            project_success = await self.initialize_project_knowledge_base()
            
            if insurance_success and project_success:
                logger.info("All knowledge bases initialized successfully")
                return True
            else:
                logger.error("Failed to initialize all knowledge bases")
                return False
                
        except Exception as e:
            logger.error(f"Error initializing all knowledge bases: {str(e)}")
            return False

# Global AI service instance
ai_service = AIService()
