# Tavily Integration for InsureWiz Chatbot

This document explains how to integrate and use Tavily web search with your InsureWiz AI chatbot to provide enhanced responses with real-time information.

## Overview

Tavily integration enhances your chatbot by combining:
- **RAG (Retrieval-Augmented Generation)**: Your existing knowledge base for foundational insurance information
- **Tavily Web Search**: Real-time web search for current information, market trends, and latest updates

## Benefits

1. **Real-time Information**: Access to current insurance rates, regulations, and market trends
2. **Enhanced Accuracy**: Combines authoritative knowledge with current data
3. **Better User Experience**: More comprehensive and up-to-date responses
4. **Fallback Support**: Gracefully degrades to RAG-only if Tavily is unavailable

## Installation

### 1. Install Dependencies

**Windows (Batch):**
```bash
install_tavily.bat
```

**Windows (PowerShell):**
```powershell
.\install_tavily.ps1
```

**Manual Installation:**
```bash
pip install tavily-python
```

### 2. Get Tavily API Key

1. Visit [https://tavily.com/](https://tavily.com/)
2. Sign up for an account
3. Get your API key from the dashboard
4. Add to your `.env` file:
   ```
   TAVILY_API_KEY=your_api_key_here
   ```

### 3. Restart Backend

After adding the API key, restart your backend server for the changes to take effect.

## Configuration

### Environment Variables

```env
# Tavily Configuration
TAVILY_API_KEY=your_api_key_here
TAVILY_SEARCH_DEPTH=basic  # basic, moderate, advanced
TAVILY_MAX_RESULTS=5
```

### Search Depth Options

- **basic**: Fast, general results (default)
- **moderate**: Balanced speed and depth
- **advanced**: Comprehensive search with more detailed results

## API Endpoints

### 1. Enhanced Chat Response

**Endpoint:** `POST /api/chat/enhanced`

**Request Body:**
```json
{
  "message": "What are the current motor insurance rates in Malaysia?",
  "session_id": "optional_session_id"
}
```

**Response:**
```json
{
  "response": "AI-generated response with RAG + Tavily information",
  "session_id": "session_id",
  "sources": [
    {
      "source": "Knowledge Base Document",
      "category": "Insurance",
      "content_preview": "..."
    },
    {
      "source": "Web Search Result",
      "category": "Web Search",
      "content_preview": "...",
      "url": "https://example.com",
      "published_date": "2024-01-15"
    }
  ],
  "rag_used": true,
  "context_docs": 3
}
```

### 2. Tavily Service Health Check

**Endpoint:** `GET /api/chat/tavily-health`

**Response:**
```json
{
  "service": "tavily",
  "status": "healthy",
  "message": "Service responding normally",
  "enabled": true
}
```

## Usage Examples

### Basic Enhanced Response

```python
from app.services.ai_service import ai_service

# Generate enhanced response with RAG + Tavily
response = await ai_service.generate_enhanced_response(
    "What are the latest changes to Malaysian insurance regulations?",
    use_tavily=True
)

print(f"Response: {response['response']}")
print(f"Web sources: {len(response['web_sources'])}")
```

### Insurance-Specific Search

```python
from app.services.tavily_service import tavily_service

# Search for insurance-related information
results = await tavily_service.search_insurance_related("motor insurance NCD")
for result in results:
    print(f"Title: {result['title']}")
    print(f"Source: {result['source']}")
    print(f"Content: {result['content'][:100]}...")
```

### Market Trends Search

```python
# Search for current market trends
trends = await tavily_service.search_market_trends("motor")
```

## How It Works

### 1. Query Analysis
The system analyzes user queries to determine if they're insurance-related and would benefit from current information.

### 2. Dual Information Retrieval
- **RAG**: Searches your knowledge base for foundational information
- **Tavily**: Performs web search for current information and trends

### 3. Context Combination
Both information sources are combined into an enhanced prompt for the AI model.

### 4. Response Generation
The AI generates a comprehensive response that:
- Uses knowledge base information for foundational facts
- Incorporates current web information for up-to-date details
- Clearly distinguishes between historical and current information

### 5. Source Attribution
All sources (both RAG and web) are included in the response for transparency.

## Fallback Behavior

If Tavily is unavailable or fails:
1. The system automatically falls back to RAG-only responses
2. Users still get helpful information from your knowledge base
3. No service interruption occurs

## Testing

Run the integration test to verify everything is working:

```bash
python test_tavily_integration.py
```

This will test:
- Tavily service availability
- Health check functionality
- Search operations
- Enhanced AI service integration

## Troubleshooting

### Common Issues

1. **"Tavily service not enabled"**
   - Check your `TAVILY_API_KEY` in the `.env` file
   - Verify the API key is valid

2. **"Service error" in health check**
   - Check your internet connection
   - Verify Tavily service status at [https://tavily.com/](https://tavily.com/)

3. **No web sources in responses**
   - Ensure Tavily is enabled
   - Check if the query is insurance-related
   - Verify search depth and result limits

### Performance Optimization

1. **Search Depth**: Use "basic" for faster responses, "advanced" for comprehensive results
2. **Result Limits**: Adjust `TAVILY_MAX_RESULTS` based on your needs
3. **Caching**: Consider implementing result caching for frequently asked questions

## Cost Considerations

- Tavily has usage-based pricing
- Monitor your usage in the Tavily dashboard
- Consider implementing rate limiting for high-traffic applications

## Security Notes

- API keys are stored in environment variables
- Web search results are filtered for quality
- No sensitive information is logged from search results

## Future Enhancements

Potential improvements:
1. **Result Caching**: Cache web search results to reduce API calls
2. **Smart Filtering**: AI-powered result relevance filtering
3. **Multi-language Support**: Enhanced search for different languages
4. **Trend Analysis**: Historical trend analysis from web data

## Support

For issues with:
- **Tavily Integration**: Check this document and run the test script
- **Tavily Service**: Visit [https://tavily.com/support](https://tavily.com/support)
- **InsureWiz Chatbot**: Check the main project documentation

