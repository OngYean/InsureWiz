from typing import List, Dict, Any, Optional
from tavily import TavilyClient
from app.config import settings
from app.utils.logger import setup_logger
from app.utils.exceptions import AIServiceException

logger = setup_logger("tavily_service")

class TavilyService:
    """Service for Tavily web search operations"""
    
    def __init__(self):
        if not settings.tavily_api_key:
            logger.warning("Tavily API key not configured")
            self.client = None
            self.enabled = False
        else:
            try:
                self.client = TavilyClient(api_key=settings.tavily_api_key)
                self.enabled = True
                logger.info("Tavily service initialized successfully")
            except Exception as e:
                logger.error(f"Failed to initialize Tavily client: {str(e)}")
                self.client = None
                self.enabled = False
    
    async def search(self, query: str, search_depth: str = None, max_results: int = None) -> List[Dict[str, Any]]:
        """
        Perform web search using Tavily
        
        Args:
            query: Search query string
            search_depth: Search depth (basic, moderate, advanced)
            max_results: Maximum number of results to return
            
        Returns:
            List of search results with metadata
        """
        if not self.enabled or not self.client:
            logger.warning("Tavily service not available")
            return []
        
        try:
            # Use configured defaults if not specified
            search_depth = search_depth or settings.tavily_search_depth
            max_results = max_results or settings.tavily_max_results
            
            logger.info(f"Performing Tavily search: '{query}' with depth '{search_depth}'")
            
            # Perform the search
            search_result = self.client.search(
                query=query,
                search_depth=search_depth,
                max_results=max_results
            )
            
            # Extract and format results
            results = self._format_search_results(search_result)
            
            logger.info(f"Tavily search completed successfully, found {len(results)} results")
            return results
            
        except Exception as e:
            logger.error(f"Error performing Tavily search: {str(e)}")
            return []
    
    async def search_insurance_related(self, query: str) -> List[Dict[str, Any]]:
        """
        Perform insurance-specific web search with enhanced context
        
        Args:
            query: Insurance-related search query
            
        Returns:
            List of relevant insurance search results
        """
        # Enhance query with insurance context for better results
        enhanced_query = f"Malaysia insurance {query} latest news regulations 2025"
        
        return await self.search(enhanced_query, search_depth="moderate", max_results=7)
    
    async def search_market_trends(self, insurance_type: str = "general") -> List[Dict[str, Any]]:
        """
        Search for current market trends and rates
        
        Args:
            insurance_type: Type of insurance (motor, home, health, life, business)
            
        Returns:
            List of market trend results
        """
        query = f"Malaysia {insurance_type} insurance market trends rates 2025 current"
        return await self.search(query, search_depth="moderate", max_results=5)
    
    async def search_regulatory_info(self, query: str) -> List[Dict[str, Any]]:
        """
        Search for regulatory and official insurance information
        
        Args:
            query: Regulatory query (e.g., "motor insurance regulations", "NCD changes")
            
        Returns:
            List of regulatory information results
        """
        # Focus on official and regulatory sources
        regulatory_domains = [
            "banknegara.gov.my",
            "piam.org.my", 
            "liam.org.my",
            "takaful.com.my",
            "insurance.com.my"
        ]
        
        enhanced_query = f"Malaysia {query} Bank Negara Malaysia BNM regulations official guidelines 2025"
        
        return await self.search(
            enhanced_query,
            search_depth="advanced",
            max_results=6,
            search_type="news",
            include_domains=regulatory_domains,
            include_answer=True,
            include_raw_content=True
        )
    
    async def search_news_and_updates(self, query: str, days_back: int = 30) -> List[Dict[str, Any]]:
        """
        Search for recent news and updates about insurance topics
        
        Args:
            query: News query
            days_back: How many days back to search
            
        Returns:
            List of recent news results
        """
        enhanced_query = f"Malaysia {query} insurance news updates {days_back} days ago 2025"
        
        return await self.search(
            enhanced_query,
            search_depth="advanced",
            max_results=8,
            search_type="news",
            include_answer=True,
            include_raw_content=True
        )
    
    def _format_search_results(self, search_result: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Format Tavily search results into standardized format"""
        formatted_results = []
        
        try:
            # Extract results from different possible response formats
            results = search_result.get('results', [])
            if not results and 'answer' in search_result:
                # Handle different response format
                results = [{'content': search_result.get('answer', '')}]
            
            for result in results:
                formatted_result = {
                    'title': result.get('title', 'No Title'),
                    'content': result.get('content', ''),
                    'url': result.get('url', ''),
                    'source': result.get('source', 'Unknown'),
                    'published_date': result.get('published_date', ''),
                    'relevance_score': result.get('score', 0.0)
                }
                
                # Filter out low-quality results
                if len(formatted_result['content']) > 50:  # Minimum content length
                    formatted_results.append(formatted_result)
            
            # Sort by relevance score (if available)
            formatted_results.sort(key=lambda x: x.get('relevance_score', 0), reverse=True)
            
        except Exception as e:
            logger.error(f"Error formatting search results: {str(e)}")
        
        return formatted_results
    
    def is_enabled(self) -> bool:
        """Check if Tavily service is available"""
        return self.enabled
    
    async def health_check(self) -> Dict[str, Any]:
        """Check Tavily service health"""
        if not self.enabled:
            return {
                "status": "disabled",
                "message": "Tavily API key not configured"
            }
        
        try:
            # Perform a simple test search
            test_results = await self.search("test", max_results=1)
            return {
                "status": "healthy",
                "message": "Service responding normally",
                "test_results_count": len(test_results)
            }
        except Exception as e:
            return {
                "status": "unhealthy",
                "message": f"Service error: {str(e)}"
            }

# Global Tavily service instance
tavily_service = TavilyService()
