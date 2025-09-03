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
from app.services.tavily_service_enhanced import enhanced_tavily_service as tavily_service

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

    async def generate_enhanced_response(self, user_message: str, use_tavily: bool = True) -> Dict[str, Any]:
        """
        Generate enhanced AI response using RAG + Tavily web search
        
        Args:
            user_message: User's question
            use_tavily: Whether to include Tavily web search (default: True)
            
        Returns:
            Enhanced response with RAG context and web search results
        """
        try:
            # Step 1: Get RAG response for foundational knowledge
            rag_response = await self.generate_rag_response(user_message)
            
            # Step 2: Get Tavily web search results if enabled and available
            tavily_results = []
            if use_tavily and tavily_service.is_enabled():
                try:
                    # Determine if this is an insurance-related query
                    if self._is_insurance_query(user_message):
                        tavily_results = await tavily_service.search_insurance_related(user_message)
                    else:
                        tavily_results = await tavily_service.search(user_message)
                    
                    logger.info(f"Tavily search returned {len(tavily_results)} results")
                except Exception as e:
                    logger.warning(f"Tavily search failed, continuing with RAG only: {str(e)}")
            
            # Step 3: Create enhanced prompt combining both sources
            enhanced_prompt = self._create_enhanced_prompt(
                user_message, 
                rag_response, 
                tavily_results
            )
            
            # Step 4: Generate final response with enhanced context
            messages = [
                SystemMessage(content=enhanced_prompt),
                HumanMessage(content=user_message)
            ]
            
            response = self.llm.invoke(messages)
            
            # Step 5: Format comprehensive response
            enhanced_response = {
                "response": response.content,
                "rag_used": True,
                "tavily_used": len(tavily_results) > 0,
                "knowledge_type": rag_response.get("knowledge_type", "none"),
                "context_docs": rag_response.get("context_docs", 0),
                "web_sources": self._format_web_sources(tavily_results),
                "rag_sources": rag_response.get("sources", []),
                "total_sources": len(rag_response.get("sources", [])) + len(tavily_results)
            }
            
            logger.info(f"Enhanced response generated successfully with RAG + Tavily")
            return enhanced_response
            
        except Exception as e:
            logger.error(f"Error generating enhanced response: {str(e)}")
            # Fallback to basic RAG response
            try:
                return await self.generate_rag_response(user_message)
            except Exception as fallback_error:
                raise AIServiceException(
                    message="Failed to generate enhanced response and fallback",
                    details={"error": str(e), "fallback_error": str(fallback_error), "user_message": user_message[:100]}
                )
    
    def _is_insurance_query(self, user_message: str) -> bool:
        """Determine if a query is insurance-related for Tavily search optimization"""
        insurance_keywords = [
            "insurance", "takaful", "policy", "coverage", "claim", "premium",
            "motor", "auto", "car", "home", "property", "health", "medical",
            "life", "family", "business", "liability", "risk", "malaysia",
            "malaysian", "ncd", "jpj", "pdrm", "bank negara", "flood",
            "rate", "price", "cost", "market", "trend", "regulation"
        ]
        
        user_message_lower = user_message.lower()
        return any(keyword in user_message_lower for keyword in insurance_keywords)
    
    def _create_enhanced_prompt(self, user_message: str, rag_response: Dict[str, Any], 
                               tavily_results: List[Dict[str, Any]]) -> str:
        """Create enhanced prompt combining RAG and Tavily results"""
        
        # Base prompt from RAG
        base_prompt = self.insurance_system_prompt
        
        # Add RAG context
        rag_context = ""
        if rag_response.get("rag_used"):
            rag_context = f"\n\nKnowledge Base Information:\n{self._format_rag_context(rag_response)}"
        
        # Add Tavily web search results
        web_context = ""
        if tavily_results:
            web_context = f"\n\nCurrent Web Information:\n{self._format_tavily_context(tavily_results)}"
        
        # Combine everything
        enhanced_prompt = f"""{base_prompt}

{rag_context}

{web_context}

User Question: {user_message}

Please provide a comprehensive answer that:
1. Uses the knowledge base information for foundational knowledge
2. Incorporates current web information for up-to-date details
3. Clearly distinguishes between historical knowledge and current information
4. Provides practical, actionable guidance
5. Always includes the disclaimer about consulting professionals

If there are conflicting information sources, prioritize the most recent and authoritative sources."""
        
        return enhanced_prompt
    
    def _format_rag_context(self, rag_response: Dict[str, Any]) -> str:
        """Format RAG response context for enhanced prompt"""
        if not rag_response.get("rag_used"):
            return "No knowledge base information available."
        
        sources = rag_response.get("sources", [])
        if not sources:
            return "Knowledge base accessed but no specific sources found."
        
        context_parts = []
        for source in sources:
            context_parts.append(f"• {source.get('source', 'Unknown')} - {source.get('category', 'General')}")
        
        return f"Knowledge Base Sources:\n" + "\n".join(context_parts)
    
    def _format_tavily_context(self, tavily_results: List[Dict[str, Any]]) -> str:
        """Format Tavily results for enhanced prompt"""
        if not tavily_results:
            return ""
        
        context_parts = []
        for i, result in enumerate(tavily_results[:3], 1):  # Limit to top 3 results
            title = result.get('title', 'No Title')
            content = result.get('content', '')[:300]  # Limit content length
            source = result.get('source', 'Unknown')
            date = result.get('published_date', '')
            
            date_info = f" ({date})" if date else ""
            context_parts.append(f"{i}. {title} - {source}{date_info}\n   {content}...")
        
        return "Current Web Sources:\n" + "\n".join(context_parts)
    
    def _classify_query_intent(self, user_message: str) -> str:
        """
        Classify user query intent to determine response strategy
        
        Args:
            user_message: User's question
            
        Returns:
            Query intent classification
        """
        try:
            # Create classification prompt
            classification_prompt = f"""
            Analyze the following user question and classify it into one of these categories:
            
            1. "project_info" - Questions about the InsureWiz project, its features, capabilities, or how to use it
            2. "insurance_current" - Questions requiring current, up-to-date insurance information, rates, or recent changes
            3. "insurance_general" - General insurance knowledge questions that don't require current information
            4. "mixed" - Questions that combine project information with current insurance knowledge needs
            5. "general" - General questions not related to insurance or the InsureWiz project (e.g., math, science, history, etc.)
            
            User Question: {user_message}
            
            Respond with ONLY the category name (e.g., "project_info", "insurance_current", etc.)
            """
            
            messages = [
                SystemMessage(content=classification_prompt),
                HumanMessage(content=user_message)
            ]
            
            response = self.llm.invoke(messages)
            intent = response.content.strip().lower()
            
            # Validate and normalize intent
            valid_intents = ["project_info", "insurance_current", "insurance_general", "mixed", "general"]
            if intent in valid_intents:
                return intent
            else:
                # Default to general insurance if classification is unclear
                logger.warning(f"Unclear query intent classification: {intent}, defaulting to insurance_general")
                return "insurance_general"
                
        except Exception as e:
            logger.error(f"Error classifying query intent: {str(e)}")
            # Default to general insurance on error
            return "insurance_general"
    
    def _format_web_sources(self, tavily_results: List[Dict[str, Any]]) -> List[Dict[str, str]]:
        """Format Tavily results for response metadata"""
        web_sources = []
        for result in tavily_results:
            web_sources.append({
                "title": result.get('title', 'No Title'),
                "url": result.get('url', ''),
                "source": result.get('source', 'Unknown'),
                "published_date": result.get('published_date', ''),
                "content_preview": result.get('content', '')[:200] + "..." if len(result.get('content', '')) > 200 else result.get('content', '')
            })
        return web_sources
    
    async def generate_intelligent_response(self, user_message: str) -> Dict[str, Any]:
        """
        Generate AI response using intelligent routing based on query intent
        
        Args:
            user_message: User's question
            
        Returns:
            Intelligent response with appropriate knowledge sources
        """
        try:
            # Step 1: Classify the query intent
            query_intent = self._classify_query_intent(user_message)
            logger.info(f"Query classified as: {query_intent}")
            
            # Step 2: Route to appropriate response strategy
            if query_intent == "project_info":
                # For project-related questions, use RAG only (no web search)
                logger.info("Using RAG-only strategy for project information query")
                return await self._generate_project_focused_response(user_message)
                
            elif query_intent == "insurance_current":
                # For current information needs, use RAG + Tavily
                logger.info("Using RAG + Tavily strategy for current insurance information")
                return await self._generate_current_insurance_response(user_message)
                
            elif query_intent == "insurance_general":
                # For general knowledge, use RAG + optional Tavily
                logger.info("Using RAG + optional Tavily strategy for general insurance knowledge")
                return await self._generate_general_insurance_response(user_message)
                
            elif query_intent == "mixed":
                # For mixed queries, use RAG + limited Tavily
                logger.info("Using mixed strategy for project + current information query")
                return await self._generate_mixed_response(user_message)
                
            elif query_intent == "general":
                # For general questions, use Gemini directly (no RAG or web search)
                logger.info("Using Gemini direct strategy for general questions")
                return await self._generate_general_question_response(user_message)
                
            else:
                # Fallback to general strategy
                logger.info("Using fallback strategy")
                return await self._generate_general_insurance_response(user_message)
                
        except Exception as e:
            logger.error(f"Error generating intelligent response: {str(e)}")
            # Fallback to basic RAG response
            try:
                return await self.generate_rag_response(user_message)
            except Exception as fallback_error:
                raise AIServiceException(
                    message="Failed to generate intelligent response and fallback",
                    details={"error": str(e), "fallback_error": str(fallback_error), "user_message": user_message[:100]}
                )
    
    async def _generate_project_focused_response(self, user_message: str) -> Dict[str, Any]:
        """Generate response focused on project information using RAG only"""
        try:
            # Use RAG with project knowledge base
            rag_response = await self.generate_rag_response(user_message)
            
            # Create enhanced project-focused prompt
            enhanced_prompt = self._create_project_focused_prompt(user_message, rag_response)
            
            # Generate final response
            messages = [
                SystemMessage(content=enhanced_prompt),
                HumanMessage(content=user_message)
            ]
            
            response = self.llm.invoke(messages)
            
            return {
                "response": response.content,
                "rag_used": True,
                "tavily_used": False,
                "knowledge_type": rag_response.get("knowledge_type", "project"),
                "context_docs": rag_response.get("context_docs", 0),
                "web_sources": [],
                "rag_sources": rag_response.get("sources", []),
                "total_sources": len(rag_response.get("sources", [])),
                "strategy": "project_focused_rag_only"
            }
            
        except Exception as e:
            logger.error(f"Error generating project-focused response: {str(e)}")
            raise
    
    async def _generate_current_insurance_response(self, user_message: str) -> Dict[str, Any]:
        """Generate response for current insurance information using RAG + Tavily"""
        try:
            # Use the existing enhanced response method
            return await self.generate_enhanced_response(user_message, use_tavily=True)
            
        except Exception as e:
            logger.error(f"Error generating current insurance response: {str(e)}")
            raise
    
    async def _generate_general_insurance_response(self, user_message: str) -> Dict[str, Any]:
        """Generate response for general insurance knowledge using RAG + optional Tavily"""
        try:
            # Use RAG first
            rag_response = await self.generate_rag_response(user_message)
            
            # Only use Tavily if RAG doesn't provide sufficient information
            if rag_response.get("context_docs", 0) < 2:  # Threshold for sufficient context
                logger.info("RAG provided limited context, adding Tavily search")
                return await self.generate_enhanced_response(user_message, use_tavily=True)
            else:
                logger.info("RAG provided sufficient context, using RAG only")
                return {
                    "response": rag_response["response"],
                    "rag_used": True,
                    "tavily_used": False,
                    "knowledge_type": rag_response.get("knowledge_type", "insurance"),
                    "context_docs": rag_response.get("context_docs", 0),
                    "web_sources": [],
                    "rag_sources": rag_response.get("sources", []),
                    "total_sources": len(rag_response.get("sources", [])),
                    "strategy": "general_insurance_rag_priority"
                }
                
        except Exception as e:
            logger.error(f"Error generating general insurance response: {str(e)}")
            raise
    
    async def _generate_mixed_response(self, user_message: str) -> Dict[str, Any]:
        """Generate response for mixed project + current information queries"""
        try:
            # Use RAG first for project information
            rag_response = await self.generate_rag_response(user_message)
            
            # Use limited Tavily for current information
            tavily_results = []
            if tavily_service.is_enabled():
                try:
                    # Limit Tavily search to 2 results for mixed queries
                    tavily_results = await tavily_service.search(user_message, max_results=2)
                    logger.info(f"Limited Tavily search returned {len(tavily_results)} results for mixed query")
                except Exception as e:
                    logger.warning(f"Tavily search failed for mixed query: {str(e)}")
            
            # Create enhanced prompt for mixed query
            enhanced_prompt = self._create_mixed_query_prompt(user_message, rag_response, tavily_results)
            
            # Generate final response
            messages = [
                SystemMessage(content=enhanced_prompt),
                HumanMessage(content=user_message)
            ]
            
            response = self.llm.invoke(messages)
            
            return {
                "response": response.content,
                "rag_used": True,
                "tavily_used": len(tavily_results) > 0,
                "knowledge_type": rag_response.get("knowledge_type", "mixed"),
                "context_docs": rag_response.get("context_docs", 0),
                "web_sources": self._format_web_sources(tavily_results),
                "rag_sources": rag_response.get("sources", []),
                "total_sources": len(rag_response.get("sources", [])) + len(tavily_results),
                "strategy": "mixed_project_current"
            }
            
        except Exception as e:
            logger.error(f"Error generating mixed response: {str(e)}")
            raise
    
    def _create_project_focused_prompt(self, user_message: str, rag_response: Dict[str, Any]) -> str:
        """Create enhanced prompt specifically for project information queries"""
        context = self._format_context(rag_response.get("sources", []))
        
        return f"""You are an AI assistant specialized in helping users understand the InsureWiz project. You have access to the project's documentation and can provide detailed information about the project structure, architecture, setup, and development.

IMPORTANT: Focus ONLY on information about the InsureWiz project itself. Do not search the web for external information unless specifically asked about external integrations or dependencies.

Project Context from Knowledge Base:
{context}

User Question: {user_message}

Please provide a comprehensive answer based on the project documentation above. Focus on:
1. Explaining the project structure and components
2. Describing how different parts work together
3. Providing setup and development guidance
4. Explaining the technical architecture and design decisions
5. Offering practical advice for development and deployment
6. Describing the features and capabilities of InsureWiz

If the documentation doesn't contain specific information about the user's question, use your general knowledge about software development and insurance systems, but clearly indicate when you're providing information from your training data versus the project documentation.

Always be helpful, clear, and provide actionable information when possible."""
    
    def _create_mixed_query_prompt(self, user_message: str, rag_response: Dict[str, Any], 
                                 tavily_results: List[Dict[str, Any]]) -> str:
        """Create enhanced prompt for mixed project + current information queries"""
        project_context = self._format_context(rag_response.get("sources", []))
        web_context = self._format_tavily_context(tavily_results)
        
        return f"""You are an AI assistant helping users understand both the InsureWiz project and current insurance information. You have access to project documentation and current web information.

Project Context from Knowledge Base:
{project_context}

Current Web Information:
{web_context}

User Question: {user_message}

Please provide a comprehensive answer that:
1. Uses the project documentation for InsureWiz-specific information
2. Incorporates current web information for up-to-date details
3. Clearly distinguishes between project features and current market information
4. Provides practical, actionable guidance
5. Balances technical project details with current insurance context

If there are conflicting information sources, prioritize the project documentation for project details and the most recent web sources for current information."""
    
    async def _generate_general_question_response(self, user_message: str) -> Dict[str, Any]:
        """Generate response for general questions using Gemini directly (no RAG or web search)"""
        try:
            # Create a general prompt for non-insurance, non-project questions
            general_prompt = f"""You are a helpful AI assistant. The user has asked a general question that is not specifically about insurance or the InsureWiz project.

User Question: {user_message}

Please provide a helpful, accurate, and informative answer to this general question. Use your knowledge and reasoning abilities to give the best possible response.

If the question is inappropriate or you cannot provide a helpful answer, please politely explain why."""
            
            messages = [
                SystemMessage(content=general_prompt),
                HumanMessage(content=user_message)
            ]
            
            response = self.llm.invoke(messages)
            
            return {
                "response": response.content,
                "rag_used": False,
                "tavily_used": False,
                "knowledge_type": "general",
                "context_docs": 0,
                "web_sources": [],
                "rag_sources": [],
                "total_sources": 0,
                "strategy": "general_gemini_direct"
            }
            
        except Exception as e:
            logger.error(f"Error generating general question response: {str(e)}")
            raise

# Global AI service instance
ai_service = AIService()
