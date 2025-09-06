# AI Chatbot Workflow Flowchart

## 🎯 Complete System Flow

```
┌─────────────────┐
│   USER QUERY    │
│                 │
│ "What are motor │
│  insurance      │
│  rates in       │
│  Malaysia?"     │
└─────────┬───────┘
          │
          ▼
┌─────────────────────────────────────────────────────────────┐
│                    API GATEWAY                              │
│              POST /api/chat/enhanced                       │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                 CHAT API ROUTER                             │
│           chat_with_enhanced_rag()                         │
│                                                             │
│  ✓ Check Tavily availability                               │
│  ✓ Route to enhanced response                              │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                AI SERVICE                                   │
│         generate_enhanced_response()                        │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│              PARALLEL PROCESSING                            │
│                                                             │
│  ┌─────────────────┐    ┌─────────────────┐               │
│  │   RAG SEARCH    │    │  TAVILY SEARCH  │               │
│  │                 │    │                 │               │
│  │ 1. Query       │    │ 1. Query        │               │
│  │    Analysis    │    │    Enhancement   │               │
│  │ 2. Knowledge   │    │ 2. Web Search   │               │
│  │    Base        │    │ 3. Result       │               │
│  │    Selection   │    │    Processing   │               │
│  │ 3. Vector      │    │ 4. Quality      │               │
│  │    Search      │    │    Filtering    │               │
│  │ 4. Context     │    │                 │               │
│  │    Formation   │    │                 │               │
│  └─────────────────┘    └─────────────────┘               │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│              CONTEXT COMBINATION                            │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │              ENHANCED PROMPT                         │   │
│  │                                                     │   │
│  │  • Base Insurance System Prompt                     │   │
│  │  • RAG Context (Knowledge Base Info)               │   │
│  │  • Tavily Context (Current Web Info)               │   │
│  │  • User Question                                    │   │
│  │  • Response Guidelines                              │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                AI GENERATION                                │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │              GOOGLE GEMINI 2.0                      │   │
│  │                                                     │   │
│  │  • Process Combined Context                         │   │
│  │  • Generate Comprehensive Response                  │   │
│  │  • Ensure Quality Standards                         │   │
│  │  • Include Required Elements                        │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│              RESPONSE ASSEMBLY                              │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │              FINAL RESPONSE                          │   │
│  │                                                     │   │
│  │  • AI-Generated Answer                              │   │
│  │  • Source Attribution (RAG + Web)                  │   │
│  │  • Metadata (Usage Stats, Source Count)            │   │
│  │  • Session Information                              │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                USER RESPONSE                                │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │              RESPONSE OBJECT                         │   │
│  │                                                     │   │
│  │  {                                                 │   │
│  │    "response": "Comprehensive answer...",          │   │
│  │    "sources": [RAG + Web sources],                 │   │
│  │    "rag_used": true,                               │   │
│  │    "tavily_used": true,                            │   │
│  │    "total_sources": 5                              │   │
│  │  }                                                 │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

## 🔄 Detailed RAG Process Flow

```
┌─────────────────┐
│  USER QUERY     │
└─────────┬───────┘
          │
          ▼
┌─────────────────────────────────────────────────────────────┐
│              KNOWLEDGE BASE SELECTION                      │
│                                                             │
│  ┌─────────────────┐    ┌─────────────────┐               │
│  │  PROJECT        │    │   INSURANCE     │               │
│  │  KEYWORDS       │    │   KEYWORDS      │               │
│  │                 │    │                 │               │
│  │  • project      │    │  • insurance    │               │
│  │  • code         │    │  • takaful      │               │
│  │  • api          │    │  • policy       │               │
│  │  • database     │    │  • motor        │               │
│  │  • setup        │    │  • health       │               │
│  └─────────────────┘    └─────────────────┘               │
│                                                             │
│  ✓ Count keyword matches                                   │
│  ✓ Select highest scoring knowledge base                   │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                VECTOR SEARCH                                │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │              PINECONE VECTOR STORE                   │   │
│  │                                                     │   │
│  │  1. Query Embedding (Google embedding-001)         │   │
│  │  2. Similarity Search (Cosine distance)            │   │
│  │  3. Result Filtering (Threshold: 0.1)              │   │
│  │  4. Top-K Results (Configurable: 5-10)             │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│              CONTEXT FORMATION                              │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │              DOCUMENT PROCESSING                     │   │
│  │                                                     │   │
│  │  • Extract page content                             │   │
│  │  • Format metadata (source, category)               │   │
│  │  • Combine into context string                      │   │
│  │  • Apply content length limits                      │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

## 🌐 Detailed Tavily Process Flow

```
┌─────────────────┐
│  USER QUERY     │
└─────────┬───────┘
          │
          ▼
┌─────────────────────────────────────────────────────────────┐
│              QUERY ENHANCEMENT                             │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │              INSURANCE QUERY DETECTION              │   │
│  │                                                     │   │
│  │  Original: "motor insurance NCD"                   │   │
│  │  Enhanced: "Malaysia insurance motor insurance     │   │
│  │           NCD latest news regulations 2025"         │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                TAVILY SEARCH                               │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │              SEARCH PARAMETERS                      │   │
│  │                                                     │   │
│  │  • Search Depth: moderate                           │   │
│  │  • Max Results: 7                                   │   │
│  │  • Query: Enhanced insurance query                  │   │
│  │  • Region: Malaysia (contextual)                    │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│              RESULT PROCESSING                             │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │              QUALITY FILTERING                      │   │
│  │                                                     │   │
│  │  • Content length > 50 characters                  │   │
│  │  • Extract title, content, URL                      │   │
│  │  • Extract source and publication date              │   │
│  │  • Sort by relevance score                          │   │
│  │  • Limit to top 3 results for context               │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

## 🚨 Fallback Mechanisms Flow

```
┌─────────────────────────────────────────────────────────────┐
│                    PRIMARY WORKFLOW                         │
│                                                             │
│  User Query → Enhanced Response (RAG + Tavily) → Response │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                  FALLBACK LAYER 1                          │
│                                                             │
│  Tavily fails → RAG-only response → Response              │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                  FALLBACK LAYER 2                          │
│                                                             │
│  RAG fails → Basic AI response → Response                 │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                  FALLBACK LAYER 3                          │
│                                                             │
│  AI fails → Error response with details                   │
└─────────────────────────────────────────────────────────────┘
```

## 📊 Performance Flow

```
┌─────────────────────────────────────────────────────────────┐
│                    RESPONSE TIMELINE                        │
│                                                             │
│  ┌─────┐  ┌─────┐  ┌─────┐  ┌─────┐  ┌─────┐            │
│  │ 0ms │  │200ms│  │700ms│  │2.7s │  │5.7s │            │
│  │     │  │     │  │     │  │     │  │     │            │
│  │User │  │RAG  │  │Tavily│  │AI   │  │Total│            │
│  │Query│  │Done │  │Done  │  │Done │  │Time │            │
│  └─────┘  └─────┘  └─────┘  └─────┘  └─────┘            │
│                                                             │
│  • RAG Processing: 200ms                                   │
│  • Tavily Search: 500ms                                   │
│  • AI Generation: 3000ms                                  │
│  • Total Response: 5.7s                                   │
└─────────────────────────────────────────────────────────────┘
```

## 🔍 Monitoring & Debugging Flow

```
┌─────────────────────────────────────────────────────────────┐
│                    LOGGING POINTS                           │
│                                                             │
│  1. Query received: [timestamp] [user_id] [query]         │
│  2. Knowledge base selected: [type] [score]               │
│  3. RAG results: [doc_count] [sources]                    │
│  4. Tavily search: [query] [results_count]                │
│  5. Context combination: [rag_context] [web_context]      │
│  6. AI generation: [start_time] [end_time]                │
│  7. Response sent: [total_time] [source_count]            │
└─────────────────────────────────────────────────────────────┘
```

## 🎯 Key Decision Points

```
┌─────────────────────────────────────────────────────────────┐
│                    DECISION TREE                            │
│                                                             │
│  User Query                                                 │
│       │                                                     │
│       ▼                                                     │
│  ┌─────────────┐                                           │
│  │ Insurance   │                                           │
│  │ Related?    │                                           │
│  └─────┬───────┘                                           │
│        │                                                   │
│        ▼                                                   │
│  ┌─────────────┐    ┌─────────────┐                       │
│  │    YES      │    │     NO      │                       │
│  │             │    │             │                       │
│  │ RAG +       │    │ RAG Only    │                       │
│  │ Tavily      │    │             │                       │
│  └─────────────┘    └─────────────┘                       │
└─────────────────────────────────────────────────────────────┘
```

This flowchart provides a comprehensive visual representation of how your AI chatbot processes queries, combining RAG and Tavily to deliver enhanced responses with multiple fallback mechanisms for reliability.

