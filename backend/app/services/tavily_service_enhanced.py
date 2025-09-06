from typing import List, Dict, Any, Optional
from tavily import TavilyClient
from app.config import settings
from app.utils.logger import setup_logger
from app.utils.exceptions import AIServiceException

logger = setup_logger("tavily_service_enhanced")

class EnhancedTavilyService:
    """Enhanced service for Tavily web search operations with advanced parameters"""
    
    def __init__(self):
        if not settings.tavily_api_key:
            logger.warning("Tavily API key not configured")
            self.client = None
            self.enabled = False
        else:
            try:
                self.client = TavilyClient(api_key=settings.tavily_api_key)
                self.enabled = True
                logger.info("Enhanced Tavily service initialized successfully")
            except Exception as e:
                logger.error(f"Failed to initialize enhanced Tavily client: {str(e)}")
                self.client = None
                self.enabled = False
    
    async def search(self, query: str, search_depth: str = None, max_results: int = None, 
                    include_domains: List[str] = None, exclude_domains: List[str] = None,
                    search_type: str = None, include_answer: bool = None, 
                    include_raw_content: bool = None) -> List[Dict[str, Any]]:
        """
        Perform web search using Tavily with advanced parameters
        
        Args:
            query: Search query string
            search_depth: Search depth (basic, advanced)
            max_results: Maximum number of results to return
            include_domains: List of domains to include in search
            exclude_domains: List of domains to exclude from search
            search_type: Type of search (news, search, places, images)
            include_answer: Include AI-generated answer
            include_raw_content: Include raw content for analysis
            
        Returns:
            List of search results with metadata
        """
        if not self.enabled or not self.client:
            logger.warning("Enhanced Tavily service not available")
            return []
        
        try:
            # Use configured defaults if not specified
            search_depth = search_depth or settings.tavily_search_depth
            max_results = max_results or settings.tavily_max_results
            include_domains = include_domains or settings.tavily_include_domains
            exclude_domains = exclude_domains or settings.tavily_exclude_domains
            search_type = search_type or settings.tavily_search_type
            include_answer = include_answer if include_answer is not None else settings.tavily_include_answer
            include_raw_content = include_raw_content if include_raw_content is not None else settings.tavily_include_raw_content
            
            logger.info(f"Performing enhanced Tavily search: '{query}' with depth '{search_depth}', type '{search_type}'")
            
            # Prepare search parameters
            search_params = {
                "query": query,
                "search_depth": search_depth,
                "max_results": max_results,
                "include_domains": include_domains,
                "exclude_domains": exclude_domains,
                "search_type": search_type,
                "include_answer": include_answer,
                "include_raw_content": include_raw_content
            }
            
            # Remove None values
            search_params = {k: v for k, v in search_params.items() if v is not None}
            
            # Perform the search
            search_result = self.client.search(**search_params)
            
            # Extract and format results
            results = self._format_search_results(search_result)
            
            logger.info(f"Enhanced Tavily search completed successfully, found {len(results)} results")
            return results
            
        except Exception as e:
            logger.error(f"Error performing enhanced Tavily search: {str(e)}")
            return []
    
    async def search_insurance_related(self, query: str) -> List[Dict[str, Any]]:
        """
        Perform insurance-specific web search with enhanced context
        
        Args:
            query: Insurance-related search query
            
        Returns:
            List of relevant insurance search results
        """
        # Smart query enhancement based on query type
        enhanced_query = self._enhance_insurance_query(query)
        
        # Use news search type for insurance queries to get latest information
        return await self.search(
            enhanced_query, 
            search_depth="advanced", 
            max_results=10,
            search_type="news",
            include_answer=True,
            include_raw_content=True
        )
    
    async def search_market_trends(self, insurance_type: str = "general") -> List[Dict[str, Any]]:
        """
        Search for current market trends and rates
        
        Args:
            insurance_type: Type of insurance (motor, home, health, life, business)
            
        Returns:
            List of market trend results
        """
        query = f"Malaysia {insurance_type} insurance market trends rates 2025 current"
        return await self.search(
            query, 
            search_depth="advanced", 
            max_results=8,
            search_type="news",
            include_answer=True,
            include_raw_content=True
        )
    
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
    
    def _enhance_insurance_query(self, query: str) -> str:
        """
        Intelligently enhance insurance queries for better search results
        
        Args:
            query: Original user query
            
        Returns:
            Enhanced query with context and keywords
        """
        query_lower = query.lower()
        
        # Base enhancement
        enhanced = f"Malaysia insurance {query}"
        
        # Add specific context based on query content
        if any(word in query_lower for word in ["motor", "car", "auto", "vehicle"]):
            enhanced += " motor vehicle insurance NCD rates premiums Bank Negara Malaysia BNM regulations"
        elif any(word in query_lower for word in ["home", "property", "house"]):
            enhanced += " home property insurance fire flood coverage Bank Negara Malaysia BNM regulations"
        elif any(word in query_lower for word in ["health", "medical", "hospital"]):
            enhanced += " health medical insurance hospital coverage Bank Negara Malaysia BNM regulations"
        elif any(word in query_lower for word in ["life", "family", "takaful"]):
            enhanced += " life family takaful insurance Bank Negara Malaysia BNM regulations"
        elif any(word in query_lower for word in ["business", "commercial", "liability"]):
            enhanced += " business commercial insurance liability coverage Bank Negara Malaysia BNM regulations"
        else:
            # General insurance query
            enhanced += " latest news regulations Bank Negara Malaysia BNM 2025"
        
        # Add time context for current information
        enhanced += " 2025 current latest"
        
        return enhanced
    
    def _format_search_results(self, search_result: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Format Tavily search results with advanced filtering and scoring"""
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
                
                # Enhanced quality filtering
                if self._is_high_quality_result(formatted_result):
                    # Calculate enhanced relevance score
                    enhanced_score = self._calculate_enhanced_score(formatted_result)
                    formatted_result['enhanced_score'] = enhanced_score
                    formatted_results.append(formatted_result)
            
            # Sort by enhanced score for better relevance
            formatted_results.sort(key=lambda x: x.get('enhanced_score', 0), reverse=True)
            
        except Exception as e:
            logger.error(f"Error formatting search results: {str(e)}")
        
        return formatted_results
    
    def _is_high_quality_result(self, result: Dict[str, Any]) -> bool:
        """Check if a search result meets quality standards"""
        content = result.get('content', '')
        title = result.get('title', '')
        url = result.get('url', '')
        
        # Minimum content length
        if len(content) < 100:
            return False
        
        # Must have a title
        if not title or title == 'No Title':
            return False
        
        # Must have a URL
        if not url:
            return False
        
        # Filter out low-quality sources
        low_quality_indicators = [
            'advertisement', 'sponsored', 'click here', 'buy now',
            'limited time', 'special offer', 'discount'
        ]
        
        content_lower = content.lower()
        title_lower = title.lower()
        
        if any(indicator in content_lower or indicator in title_lower for indicator in low_quality_indicators):
            return False
        
        return True
    
    def _calculate_enhanced_score(self, result: Dict[str, Any]) -> float:
        """Calculate enhanced relevance score for better result ranking"""
        base_score = result.get('relevance_score', 0.0)
        content = result.get('content', '')
        title = result.get('title', '')
        url = result.get('url', '')
        
        enhanced_score = base_score
        
        # Boost for Malaysian domains
        malaysian_domains = ['.my', 'banknegara.gov.my', 'piam.org.my', 'liam.org.my']
        if any(domain in url for domain in malaysian_domains):
            enhanced_score += 0.3
        
        # Boost for recent content (if date available)
        if result.get('published_date'):
            enhanced_score += 0.2
        
        # Boost for comprehensive content
        if len(content) > 500:
            enhanced_score += 0.1
        
        # Boost for insurance-specific keywords in title
        insurance_keywords = ['insurance', 'takaful', 'premium', 'coverage', 'claim', 'policy']
        title_lower = title.lower()
        keyword_matches = sum(1 for keyword in insurance_keywords if keyword in title_lower)
        enhanced_score += keyword_matches * 0.05
        
        # Boost for regulatory/authoritative sources
        authoritative_sources = ['bank negara', 'bnm', 'piam', 'liam', 'government', 'official']
        content_lower = content.lower()
        auth_matches = sum(1 for source in authoritative_sources if source in content_lower)
        enhanced_score += auth_matches * 0.05
        
        return min(enhanced_score, 1.0)  # Cap at 1.0
    
    def is_enabled(self) -> bool:
        """Check if enhanced Tavily service is available"""
        return self.enabled
    
    async def health_check(self) -> Dict[str, Any]:
        """Check enhanced Tavily service health"""
        if not self.enabled:
            return {
                "status": "disabled",
                "message": "Enhanced Tavily API key not configured"
            }
        
        try:
            # Perform a simple test search
            test_results = await self.search("test", max_results=1)
            return {
                "status": "healthy",
                "message": "Enhanced service responding normally",
                "test_results_count": len(test_results)
            }
        except Exception as e:
            return {
                "status": "unhealthy",
                "message": f"Enhanced service error: {str(e)}"
            }

# Global enhanced Tavily service instance
enhanced_tavily_service = EnhancedTavilyService()

