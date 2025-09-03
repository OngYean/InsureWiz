# AI Chatbot Workflow: From User Query to Response

This document provides a comprehensive overview of how the InsureWiz AI chatbot processes user queries, combining RAG (Retrieval-Augmented Generation) with Tavily web search to deliver enhanced responses.

## 🚀 Complete Workflow Overview

```
User Query → API Gateway → AI Service → RAG + Tavily → Response Generation → User
```

## 📋 Detailed Workflow Steps

### 1. **User Input & API Gateway**
```
User sends query → POST /api/chat/enhanced → Chat API Router
```

**Input Example:**
```json
{
  "message": "What are the current motor insurance rates in Malaysia for 2024?",
  "session_id": "user_session_123"
}
```

### 2. **Query Analysis & Routing**
```
Chat API → AI Service → Query Analysis → Route to Enhanced Response
```

**Process:**
- API receives request at `/api/chat/enhanced`
- Routes to `chat_with_enhanced_rag()` function
- Checks if Tavily service is available
- Falls back to RAG-only if Tavily unavailable

### 3. **Enhanced Response Generation**
```
AI Service → generate_enhanced_response() → RAG + Tavily Integration
```

**Step-by-Step Process:**

#### 3.1 **RAG Response Generation**
```
generate_rag_response() → Knowledge Base Selection → Document Retrieval
```

**Knowledge Base Selection Logic:**
```python
def _determine_knowledge_base(user_message: str):
    # Count keyword matches
    project_score = count_project_keywords(user_message)
    insurance_score = count_insurance_keywords(user_message)
    
    if project_score > insurance_score:
        return "project", search_project_knowledge()
    elif insurance_score > 0:
        return "insurance", search_insurance_knowledge()
    else:
        return "none", []
```

**Document Retrieval:**
```
Vector Store → Similarity Search → Top-K Results → Context Formation
```

**Vector Search Process:**
1. **Query Embedding**: Convert user query to vector using Google's embedding-001 model
2. **Similarity Search**: Search Pinecone vector store for similar documents
3. **Result Filtering**: Apply similarity threshold (0.1) and limit to top-K results
4. **Context Formation**: Format retrieved documents into context string

#### 3.2 **Tavily Web Search**
```
Tavily Service → Query Enhancement → Web Search → Result Processing
```

**Insurance Query Enhancement:**
```python
# Original: "motor insurance NCD"
# Enhanced: "Malaysia insurance motor insurance NCD latest news regulations 2025"
enhanced_query = f"Malaysia insurance {query} latest news regulations 2025"
```

**Web Search Process:**
1. **Query Analysis**: Determine if insurance-related using keyword matching
2. **Search Execution**: Perform Tavily search with appropriate depth and result limits
3. **Result Formatting**: Extract title, content, URL, source, and publication date
4. **Quality Filtering**: Filter out low-quality results (content < 50 characters)

### 4. **Context Combination & Prompt Engineering**
```
RAG Context + Tavily Results → Enhanced Prompt → AI Model Input
```

**Enhanced Prompt Structure:**
```
Base Insurance System Prompt
+
Knowledge Base Information (RAG)
+
Current Web Information (Tavily)
+
User Question
+
Response Guidelines
```

**Prompt Example:**
```
You are an Expert AI Insurance Advisor specialized in Malaysian insurance and Takaful policies...

Knowledge Base Information:
• Motor Insurance Guide - Insurance
• NCD Calculation Guide - Insurance

Current Web Information:
1. Latest Motor Insurance Rates 2025 - Insurance.com (2025-01-15)
   Current market trends show increasing rates due to...

User Question: What are the current motor insurance rates in Malaysia for 2024?

Please provide a comprehensive answer that:
1. Uses the knowledge base information for foundational knowledge
2. Incorporates current web information for up-to-date details
3. Clearly distinguishes between historical knowledge and current information
4. Provides practical, actionable guidance
5. Always includes the disclaimer about consulting professionals
```

### 5. **AI Response Generation**
```
Enhanced Prompt → Google Gemini 2.0 → Response Generation → Formatting
```

**AI Model Process:**
1. **Context Processing**: Model processes combined RAG + Tavily context
2. **Response Generation**: Generate comprehensive answer using Gemini 2.0
3. **Quality Assurance**: Ensure response includes required elements (disclaimer, etc.)

### 6. **Response Assembly & Metadata**
```
AI Response + Source Attribution + Metadata → Final Response Object
```

**Response Structure:**
```json
{
  "response": "AI-generated comprehensive answer...",
  "session_id": "user_session_123",
  "sources": [
    {
      "source": "Motor Insurance Guide",
      "category": "Insurance",
      "content_preview": "Comprehensive guide to motor insurance..."
    },
    {
      "source": "Latest Motor Insurance Rates 2025",
      "category": "Web Search",
      "content_preview": "Current market trends show...",
      "url": "https://insurance.com/rates-2025",
      "published_date": "2025-01-15"
    }
  ],
  "rag_used": true,
  "context_docs": 2,
  "tavily_used": true,
  "web_sources": [...],
  "total_sources": 3
}
```

## 🔄 Fallback Mechanisms

### **Primary Fallback (Tavily → RAG)**
```
Tavily fails → Continue with RAG only → Generate response
```

### **Secondary Fallback (RAG → Basic)**
```
RAG fails → Basic AI response → Return simple answer
```

### **Tertiary Fallback (AI → Error)**
```
AI generation fails → Return error with fallback details
```

## 📊 Performance Metrics & Monitoring

### **Response Time Breakdown:**
- **RAG Processing**: ~200-500ms (vector search + context formation)
- **Tavily Search**: ~500-2000ms (web search + result processing)
- **AI Generation**: ~1000-3000ms (context processing + response generation)
- **Total Response Time**: ~2-6 seconds

### **Quality Metrics:**
- **Source Diversity**: RAG + Web sources
- **Information Freshness**: Historical + Current data
- **Response Completeness**: Comprehensive coverage
- **Source Attribution**: Transparent source listing

## 🎯 Optimization Strategies

### **1. Parallel Processing**
```
RAG Search ─┐
             ├─→ Context Combination → AI Generation
Tavily Search ─┘
```

### **2. Caching Strategy**
- **RAG Results**: Cache frequent queries
- **Tavily Results**: Cache web search results (TTL: 1 hour)
- **AI Responses**: Cache similar queries

### **3. Smart Query Routing**
- **Insurance Queries**: Full RAG + Tavily
- **Project Queries**: RAG only (no web search needed)
- **General Queries**: Basic AI response

## 🚨 Error Handling & Resilience

### **Error Scenarios:**
1. **Tavily Service Unavailable**: Fallback to RAG-only
2. **Vector Store Issues**: Fallback to basic AI response
3. **AI Model Errors**: Return cached responses or error message
4. **Network Issues**: Graceful degradation with available services

### **Resilience Features:**
- **Automatic Fallbacks**: Multiple fallback layers
- **Service Health Checks**: Monitor all service components
- **Circuit Breaker**: Prevent cascade failures
- **Retry Logic**: Automatic retry for transient failures

## 🔍 Debugging & Monitoring

### **Key Log Points:**
```
1. Query received: [timestamp] [user_id] [query]
2. Knowledge base selected: [type] [score]
3. RAG results: [doc_count] [sources]
4. Tavily search: [query] [results_count]
5. Context combination: [rag_context] [web_context]
6. AI generation: [start_time] [end_time]
7. Response sent: [total_time] [source_count]
```

### **Health Check Endpoints:**
- `GET /api/chat/tavily-health` - Tavily service status
- `GET /api/health` - Overall system health
- `GET /api/chat/vector-store-stats` - Vector store statistics

## 📈 Future Enhancements

### **Planned Improvements:**
1. **Result Caching**: Redis-based caching for web search results
2. **Smart Filtering**: AI-powered result relevance scoring
3. **Multi-language Support**: Enhanced search for different languages
4. **Trend Analysis**: Historical trend analysis from web data
5. **Response Optimization**: Dynamic prompt engineering based on query type

### **Performance Targets:**
- **Response Time**: Reduce to 1-3 seconds
- **Accuracy**: Improve source relevance scoring
- **Scalability**: Support 1000+ concurrent users
- **Cost Optimization**: Reduce API calls through smart caching

## 🎯 Summary

The InsureWiz AI chatbot workflow is a sophisticated, multi-layered system that:

1. **Intelligently routes** queries to appropriate knowledge bases
2. **Combines** static knowledge (RAG) with real-time information (Tavily)
3. **Generates** comprehensive responses using Google Gemini 2.0
4. **Provides** transparent source attribution for all information
5. **Maintains** high availability through multiple fallback mechanisms
6. **Optimizes** performance through parallel processing and caching
7. **Monitors** system health and performance metrics

This architecture ensures users receive accurate, current, and comprehensive insurance information while maintaining system reliability and performance.

