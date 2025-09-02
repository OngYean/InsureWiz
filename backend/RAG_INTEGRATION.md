# InsureWiz RAG Integration Guide

## Overview

This guide explains how to set up and use the Retrieval-Augmented Generation (RAG) system integrated with Pinecone vector database in InsureWiz. The RAG system enhances the AI chatbot by providing access to a knowledge base of Malaysian insurance and Takaful information.

## Features

- **Vector Database**: Pinecone integration for efficient document storage and retrieval
- **Knowledge Base**: Pre-loaded Malaysian insurance knowledge base
- **Smart Retrieval**: Semantic search for relevant information
- **Enhanced Responses**: AI responses augmented with knowledge base context
- **Fallback System**: Automatic fallback to basic AI responses if RAG fails
- **Source Attribution**: Track which knowledge base sources were used

## Architecture

```
User Query → RAG System → Pinecone Vector Store → Knowledge Base Search → Context Retrieval → Enhanced AI Response
```

### Components

1. **Vector Store Service** (`vector_store.py`): Manages Pinecone operations
2. **Document Service** (`document_service.py`): Handles knowledge base management
3. **AI Service** (`ai_service.py`): Integrates RAG with AI responses
4. **Chat API** (`chat.py`): Provides RAG-enabled chat endpoints

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Environment Configuration

Create a `.env` file in the backend directory:

```env
# Google AI Configuration
GOOGLE_API_KEY=your_google_api_key_here
GOOGLE_MODEL_NAME=gemini-2.0-flash
GOOGLE_TEMPERATURE=0.7

# Pinecone Configuration
PINECONE_API_KEY=your_pinecone_api_key_here
PINECONE_ENVIRONMENT=gcp-starter
PINECONE_INDEX_NAME=insurewiz

# Server Configuration
HOST=0.0.0.0
PORT=8000
DEBUG=false
```

### 3. Pinecone Setup

1. **Get API Key**: Use the provided Pinecone API key
2. **Environment**: The system uses `gcp-starter` (free tier)
3. **Index**: Automatically creates `insurewiz` index

### 4. Start the Server

```bash
# Development
python run.py

# Production
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## API Endpoints

### Basic Chat (No RAG)
```http
POST /api/chat/
Content-Type: application/json

{
  "message": "What is insurance?",
  "session_id": "optional_session_id"
}
```

### RAG-Enabled Chat
```http
POST /api/chat/rag
Content-Type: application/json

{
  "message": "Explain NCD in Malaysian motor insurance",
  "session_id": "optional_session_id",
  "namespace": "insurance_knowledge"
}
```

### Initialize Knowledge Base
```http
POST /api/chat/initialize-knowledge
```

### Get Knowledge Base Stats
```http
GET /api/chat/knowledge-stats
```

### Check RAG Status
```http
GET /api/chat/rag-status
```

## Knowledge Base Content

The system comes pre-loaded with comprehensive Malaysian insurance knowledge:

### Categories
- **Motor Insurance**: Coverage types, NCD system, claims process
- **Home Insurance**: Fire, contents, liability, natural disasters
- **Health Insurance**: Hospitalization, panel hospitals, critical illness
- **Life Insurance**: Term, whole life, investment-linked, riders
- **Claims Process**: Documentation, timelines, dispute resolution
- **Regulations**: BNM guidelines, consumer protection, compliance

### Document Structure
```python
Document(
    page_content="Insurance information...",
    metadata={
        "source": "malaysian_insurance_guide",
        "category": "motor_insurance",
        "language": "english"
    }
)
```

## Usage Examples

### Python Client

```python
import requests

# RAG-enabled chat
response = requests.post("http://localhost:8000/api/chat/rag", json={
    "message": "What documents do I need for motor insurance claims?",
    "namespace": "insurance_knowledge"
})

print(f"Response: {response.json()['response']}")
print(f"Sources: {response.json()['sources']}")
print(f"RAG used: {response.json()['rag_used']}")
```

### JavaScript/TypeScript Client

```typescript
// RAG-enabled chat
const response = await fetch("http://localhost:8000/api/chat/rag", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({
    message: "Explain comprehensive motor insurance coverage",
    namespace: "insurance_knowledge"
  })
});

const data = await response.json();
console.log("Response:", data.response);
console.log("Sources:", data.sources);
console.log("RAG used:", data.rag_used);
```

## Testing

### Run Test Script

```bash
cd backend
python test_rag.py
```

### Manual Testing

1. **Start server**: `python run.py`
2. **Initialize knowledge base**: `POST /api/chat/initialize-knowledge`
3. **Test RAG chat**: `POST /api/chat/rag` with insurance questions
4. **Check status**: `GET /api/chat/rag-status`

## Configuration Options

### Vector Store Settings
```python
# In config.py
chunk_size: int = 1000          # Document chunk size
chunk_overlap: int = 200        # Overlap between chunks
top_k_results: int = 5          # Number of results to retrieve
```

### Pinecone Settings
```python
# In config.py
pinecone_environment: str = "gcp-starter"     # Pinecone environment
pinecone_index_name: str = "insurewiz"        # Index name
```

## Monitoring and Debugging

### Logs
- **Vector Store**: Pinecone operations and errors
- **Document Service**: Knowledge base management
- **AI Service**: RAG chain operations and fallbacks

### Health Checks
- **RAG Status**: `GET /api/chat/rag-status`
- **Knowledge Stats**: `GET /api/chat/knowledge-stats`
- **General Health**: `GET /api/chat/health`

### Common Issues

1. **Pinecone Connection Failed**
   - Check API key and environment
   - Verify internet connection
   - Check Pinecone service status

2. **Knowledge Base Initialization Failed**
   - Check Pinecone connection
   - Verify API permissions
   - Check log files for errors

3. **RAG Responses Not Working**
   - Verify knowledge base is initialized
   - Check RAG chain status
   - Review error logs

## Performance Optimization

### Chunking Strategy
- **Optimal chunk size**: 1000 characters with 200 character overlap
- **Balances**: Retrieval accuracy vs. context relevance

### Caching
- **Vector store**: Pinecone handles vector caching
- **Response caching**: Consider implementing for frequent queries

### Scaling
- **Pinecone**: Upgrade to paid plan for higher limits
- **Index optimization**: Adjust dimensions and metrics as needed

## Security Considerations

1. **API Keys**: Store securely in environment variables
2. **Access Control**: Implement authentication for production use
3. **Data Privacy**: Ensure compliance with data protection regulations
4. **Rate Limiting**: Consider implementing request throttling

## Future Enhancements

1. **Multi-language Support**: Add Malay and Chinese knowledge base
2. **Dynamic Updates**: Real-time knowledge base updates
3. **User Feedback**: Learn from user interactions
4. **Advanced Retrieval**: Implement hybrid search strategies
5. **Analytics**: Track query patterns and knowledge gaps

## Support

For issues or questions:
1. Check the logs for error details
2. Verify configuration settings
3. Test with the provided test script
4. Review Pinecone documentation
5. Check InsureWiz project documentation

## License

This RAG integration is part of the InsureWiz project and follows the same licensing terms.
