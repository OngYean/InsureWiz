# InsureWiz AI Integration Guide

## Overview
InsureWiz integrates with Google Gemini Pro through LangChain to provide intelligent insurance assistance. This guide explains the AI integration architecture and configuration.

## AI Architecture

### System Components
```
User Input → Frontend Chat → Backend API → LangChain Service → Google Gemini → Response Processing → User
```

### Key Technologies
- **LangChain**: AI orchestration and conversation management
- **Google Gemini Pro**: Large language model for intelligent responses
- **FastAPI**: Backend API framework
- **Pydantic**: Data validation and serialization

## Configuration

### 1. Google AI Studio Setup
1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in and create API key
3. Add to backend `.env` file:
```env
GOOGLE_API_KEY=your_google_api_key_here
GOOGLE_MODEL_NAME=gemini-pro
GOOGLE_MAX_TOKENS=1000
GOOGLE_TEMPERATURE=0.7
```

### 2. LangChain Configuration
```python
from langchain_google_genai import ChatGoogleGenerativeAI

class AIService:
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-pro",
            google_api_key=settings.GOOGLE_API_KEY,
            temperature=0.7,
            max_output_tokens=1000
        )
```

## AI Service Implementation

### Core Chat Service
```python
class ChatService:
    def __init__(self):
        self.ai_service = AIService()
        self.conversation_store = {}
    
    async def process_message(self, message: ChatMessage, conversation_id: str = None) -> ChatResponse:
        # Get conversation context
        conversation = self._get_conversation(conversation_id)
        
        # Generate AI response
        ai_response = await self._generate_ai_response(message.content, conversation)
        
        # Save conversation
        self._save_conversation(conversation_id, conversation)
        
        return ChatResponse(
            response=ai_response["response"],
            conversation_id=conversation_id,
            timestamp=ai_response["timestamp"]
        )
```

### Prompt Engineering
```python
INSURANCE_SYSTEM_PROMPT = """
You are an Expert AI Insurance Advisor specialized in Malaysian insurance and Takaful policies. You have deep knowledge of insurance coverage types, claims processes, and risk management practices relevant to Malaysia.

Your role is to:
1. Provide accurate and helpful information about Malaysian insurance concepts
2. Explain complex insurance terms in simple, understandable language, using local examples when possible
3. Offer general guidance on insurance and Takaful decisions (but never specific financial advice)
4. Help users understand their coverage options and policy details, including common Malaysian exclusions and riders
5. Guide users through claims processes and documentation requirements in Malaysia (e.g., JPJ/PDRM reports for motor claims, Bank Negara guidelines for disputes)
6. Explain factors affecting insurance premiums in Malaysia, such as No Claim Discount (NCD), sum insured, driver's age, flood coverage, and location-based risks

Key Areas of Expertise in Malaysia:
- Motor/Auto Insurance & Takaful (third-party, comprehensive, windscreen, special perils, NCD)
- Home/Property Insurance & Takaful (fire, contents, liability, mortgage protection)
- Health Insurance & Medical Takaful (hospitalisation, critical illness, panel hospitals, deductibles, co-pays)
- Life Insurance & Family Takaful (term, whole life, investment-linked, riders, MRTA/MLTA)
- Business Insurance (general liability, professional indemnity, workers' compensation, SME packages)
- Claims Processes (reporting timelines, required documents, repair approvals, hospital claims)
- Risk Management (personal and business risk reduction strategies in Malaysia's context)

Language Support:
- Support Malay (Bahasa Malaysia), English, and Chinese (Simplified or Traditional)
- Always respond in the language of the user's query
- If unclear, politely ask which language they prefer

⚠️ IMPORTANT DISCLAIMER: This information is for general purposes only. Please consult a licensed insurance or Takaful professional in Malaysia for advice specific to your policy and coverage needs.
"""
```

## Conversation Management

### Context Management
```python
class ConversationContextManager:
    def __init__(self, max_context_length: int = 4000):
        self.max_context_length = max_context_length
    
    def truncate_conversation(self, conversation: List[Dict]) -> List[Dict]:
        """Truncate conversation to fit within context window."""
        # Implementation for managing conversation length
        pass
```

## Performance Optimization

### Response Caching
```python
class ResponseCache:
    def __init__(self, max_size: int = 1000):
        self.cache = {}
        self.max_size = max_size
    
    def get(self, key: str) -> Optional[Dict]:
        return self.cache.get(key)
    
    def set(self, key: str, response: Dict, ttl: int = 3600):
        if len(self.cache) >= self.max_size:
            self._evict_oldest()
        self.cache[key] = response
```

## Monitoring and Analytics

### Performance Metrics
```python
class AIMetricsCollector:
    def __init__(self):
        self.metrics = {
            "response_times": [],
            "success_rate": 0,
            "total_requests": 0
        }
    
    def record_request(self, start_time: float, end_time: float, success: bool):
        response_time = end_time - start_time
        self.metrics["response_times"].append(response_time)
        self.metrics["total_requests"] += 1
```

## Best Practices

### 1. Prompt Engineering
- Use clear, specific instructions
- Include examples when possible
- Set appropriate temperature and token limits
- Test prompts with various inputs

### 2. Error Handling
- Implement graceful fallbacks
- Log errors for debugging
- Provide user-friendly error messages
- Monitor for common failure patterns

### 3. Security
- Validate all inputs
- Sanitize AI responses
- Implement rate limiting
- Monitor for abuse patterns

### 4. Performance
- Cache frequently requested responses
- Use async processing
- Implement response streaming
- Monitor response times

## Troubleshooting

### Common Issues
1. **API Key Problems**: Verify key validity and permissions
2. **Response Quality**: Review and refine prompts
3. **Performance**: Implement caching and async processing
4. **Conversation Management**: Handle context properly

### Getting Help
1. Check Google AI Studio documentation
2. Review LangChain documentation
3. Monitor application logs
4. Test with different prompts
