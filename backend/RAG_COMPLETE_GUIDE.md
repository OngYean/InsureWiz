# InsureWiz RAG Complete System Guide

## Overview

This guide covers the complete RAG (Retrieval-Augmented Generation) system for InsureWiz, now configured to use the **insurewiz768** Pinecone index. The system provides intelligent knowledge retrieval and AI-powered responses for both insurance knowledge and project documentation.

## 🏗️ System Architecture

### Components

1. **Vector Store Service** (`vector_store.py`)
   - Manages Pinecone vector database operations
   - Handles document ingestion and similarity search
   - Supports multiple namespaces for different knowledge domains

2. **AI Service** (`ai_service.py`)
   - Integrates Google Gemini AI model
   - Provides RAG-enhanced responses
   - Intelligently selects knowledge bases based on query content

3. **Document Services**
   - **Insurance Document Service** (`document_service.py`): Manages Malaysian insurance knowledge
   - **Project Document Service** (`project_document_service.py`): Handles project documentation

4. **Embedding Service** (`embedding_service.py`)
   - Generates vector embeddings for documents and queries
   - Uses Google's embedding model for high-quality representations

## 🔧 Configuration

### Environment Variables

```bash
# Pinecone Configuration
PINECONE_API_KEY=your_api_key_here
PINECONE_ENVIRONMENT=gcp-starter
PINECONE_INDEX_NAME=insurewiz768

# Google AI Configuration
GOOGLE_API_KEY=your_google_api_key_here

# Server Configuration
HOST=0.0.0.0
PORT=8000
DEBUG=false
```

### RAG Settings

```python
# Chunking Configuration
chunk_size = 1000          # Characters per chunk
chunk_overlap = 200        # Overlap between chunks
top_k_results = 5          # Number of results to retrieve
```

## 🚀 Quick Start

### 1. Setup Dependencies

```bash
# Run the setup script
setup_rag_complete.bat

# Or manually install
pip install -r requirements.txt
```

### 2. Test the Complete System

```bash
# Run the comprehensive test suite
test_rag_complete.bat

# Or use PowerShell
test_rag_complete.ps1

# Or run directly
python test_rag_complete.py
```

### 3. Start the Server

```bash
# Start the FastAPI server
python main.py

# Or use the batch file
start.bat
```

## 📚 Knowledge Base Structure

### Namespaces

- **`insurance_knowledge`**: Malaysian insurance and Takaful information
- **`project_knowledge`**: InsureWiz project documentation and setup guides

### Document Types

#### Insurance Knowledge
- Motor/Auto Insurance Coverage
- Home/Property Insurance
- Health Insurance & Medical Takaful
- Life Insurance & Family Takaful
- Claims Process Guidelines
- Regulatory Compliance

#### Project Knowledge
- Project Overview & Architecture
- Setup & Installation Guides
- API Documentation
- Development Guidelines
- Technical Features

## 🔍 Similarity Search Features

### Intelligent Query Routing

The system automatically determines which knowledge base to search based on query keywords:

- **Insurance-related queries** → `insurance_knowledge` namespace
- **Project-related queries** → `project_knowledge` namespace
- **Ambiguous queries** → Searches both namespaces

### Search Capabilities

- **Namespace-specific search**: Search within specific knowledge domains
- **Cross-namespace search**: Search across all knowledge bases
- **Semantic similarity**: Find relevant documents even with different wording
- **Metadata filtering**: Filter by source, category, and language

## 🤖 AI Response Generation

### RAG-Enhanced Responses

1. **Query Analysis**: Determine knowledge base and search strategy
2. **Document Retrieval**: Find relevant documents using similarity search
3. **Context Enhancement**: Create AI prompts with retrieved knowledge
4. **Response Generation**: Generate comprehensive, knowledge-based responses

### Response Types

- **RAG Responses**: Enhanced with retrieved knowledge base information
- **Fallback Responses**: Basic AI responses when knowledge base search fails
- **Contextual Responses**: Responses that consider conversation history

## 🧪 Testing & Validation

### Test Suite Coverage

The complete test suite validates:

1. **Index Connection**: Pinecone index connectivity and configuration
2. **Embedding Service**: Document and query embedding generation
3. **Knowledge Base Ingestion**: Document processing and storage
4. **Similarity Search Completeness**: Search accuracy across domains
5. **RAG Response Generation**: AI response quality and knowledge integration
6. **Cross-Namespace Search**: Multi-domain knowledge retrieval

### Running Tests

```bash
# Complete test suite
python test_rag_complete.py

# Individual test files
python test_similarity_search.py
python test_rag_system.py
python test_rag_debug.py
```

## 📊 Performance Metrics

### Completeness Scoring

- **80%+**: Excellent - Ready for production
- **60-79%**: Good - Minor improvements needed
- **<60%**: Needs attention - Review and fix issues

### Key Metrics

- **Similarity Search Completeness**: Percentage of successful searches
- **RAG Effectiveness**: Percentage of RAG-enhanced responses
- **Response Quality**: Relevance and accuracy of AI responses
- **Search Speed**: Query response time

## 🔧 Troubleshooting

### Common Issues

1. **Index Connection Failures**
   - Verify Pinecone API key and environment
   - Check index name matches configuration
   - Ensure index exists in Pinecone console

2. **Embedding Generation Errors**
   - Verify Google API key configuration
   - Check internet connectivity
   - Validate API quotas and limits

3. **Document Ingestion Failures**
   - Check file permissions and paths
   - Verify document format and encoding
   - Review chunking parameters

4. **Search Quality Issues**
   - Adjust similarity thresholds
   - Review chunk size and overlap settings
   - Check document preprocessing quality

### Debug Mode

Enable debug logging by setting `DEBUG=true` in your `.env` file for detailed error information.

## 🚀 Production Deployment

### Prerequisites

- ✅ Pinecone index configured and accessible
- ✅ Google AI API key with sufficient quotas
- ✅ All dependencies installed and tested
- ✅ Knowledge bases populated with quality content
- ✅ Test suite passing with high scores

### Monitoring

- Monitor API response times
- Track similarity search success rates
- Monitor AI response quality
- Check Pinecone index performance

## 📈 Future Enhancements

### Planned Features

- **Multi-language Support**: Malay, English, Chinese
- **Advanced Filtering**: Date, source, and category-based filtering
- **Response Caching**: Improve response times for common queries
- **Knowledge Base Analytics**: Usage patterns and content effectiveness
- **Automated Updates**: Scheduled knowledge base refresh

### Integration Opportunities

- **Chatbot Interface**: Direct integration with frontend
- **API Endpoints**: RESTful API for external access
- **Webhook Support**: Real-time knowledge updates
- **Analytics Dashboard**: Performance monitoring and insights

## 📞 Support

For issues or questions about the RAG system:

1. Check the troubleshooting section above
2. Review test results for specific failure points
3. Check logs for detailed error information
4. Verify configuration and environment setup

---

**Last Updated**: December 2024  
**Version**: 1.0.0  
**Index**: insurewiz768

