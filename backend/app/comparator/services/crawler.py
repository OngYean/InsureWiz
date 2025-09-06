"""
Web crawling service using Tavily API for URL discovery and Crawl4AI for content extraction
"""

import asyncio
import logging
from typing import List, Dict, Any, Optional
import os
import requests
from urllib.parse import urljoin, urlparse
import time

logger = logging.getLogger(__name__)

class TavilyDiscovery:
    """URL discovery using Tavily API"""
    
    def __init__(self):
        self.api_key = os.getenv("TAVILY_API_KEY")
        self.base_url = "https://api.tavily.com/search"
        
        if not self.api_key:
            logger.warning("Tavily API key not found. URL discovery will be limited.")
    
    def discover_urls(self, search_terms: List[str], max_results: int = 5) -> List[str]:
        """Discover URLs using Tavily search"""
        if not self.api_key:
            logger.warning("Tavily API not available, returning empty results")
            return []
        
        all_urls = []
        
        for term in search_terms:
            try:
                urls = self._search_single_term(term, max_results)
                all_urls.extend(urls)
                
                # Add small delay to respect rate limits
                time.sleep(0.5)
                
            except Exception as e:
                logger.error(f"Error searching for '{term}': {e}")
                continue
        
        # Remove duplicates and return
        unique_urls = list(set(all_urls))
        logger.info(f"Discovered {len(unique_urls)} unique URLs from {len(search_terms)} search terms")
        
        return unique_urls
    
    def _search_single_term(self, search_term: str, max_results: int) -> List[str]:
        """Search for a single term using Tavily"""
        try:
            payload = {
                "api_key": self.api_key,
                "query": search_term,
                "search_depth": "basic",
                "include_answer": False,
                "include_images": False,
                "include_raw_content": False,
                "max_results": max_results,
                "include_domains": [
                    "zurich.com.my",
                    "etiqa.com.my", 
                    "allianz.com.my",
                    "axa.com.my",
                    "generali.com.my",
                    "libertyinsurance.com.my",
                    "amgeneral.com",
                    "takaful-ikhlas.com.my",
                    "berjayasompo.com.my",
                    "tokiomarine.com",
                    "greateastern.com.my"
                ]
            }
            
            response = requests.post(self.base_url, json=payload, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            
            # Extract URLs from results
            urls = []
            for result in data.get("results", []):
                url = result.get("url")
                if url and self._is_valid_insurance_url(url):
                    urls.append(url)
            
            logger.debug(f"Found {len(urls)} URLs for term: {search_term}")
            return urls
            
        except requests.RequestException as e:
            logger.error(f"HTTP error in Tavily search: {e}")
            return []
        except Exception as e:
            logger.error(f"Unexpected error in Tavily search: {e}")
            return []
    
    def _is_valid_insurance_url(self, url: str) -> bool:
        """Check if URL is relevant for insurance content"""
        url_lower = url.lower()
        
        # Must contain insurance-related keywords
        insurance_keywords = ['motor', 'car', 'vehicle', 'insurance', 'takaful', 'comprehensive']
        
        if not any(keyword in url_lower for keyword in insurance_keywords):
            return False
        
        # Exclude unwanted pages
        exclude_keywords = ['blog', 'news', 'career', 'contact', 'about', 'login', 'register']
        
        if any(keyword in url_lower for keyword in exclude_keywords):
            return False
        
        return True

class Crawl4AIExtractor:
    """Content extraction using Crawl4AI (stub implementation)"""
    
    def __init__(self):
        # For now, this is a stub. In production, you would:
        # from crawl4ai import WebCrawler
        # self.crawler = WebCrawler()
        logger.warning("Crawl4AI not implemented. Using stub extractor.")
    
    async def extract_content(self, urls: List[str]) -> Dict[str, str]:
        """Extract content from URLs"""
        # Stub implementation - in production this would use Crawl4AI
        logger.warning("Using stub content extraction")
        
        content_results = {}
        
        for url in urls:
            try:
                # Simulate content extraction
                content_results[url] = await self._extract_single_url(url)
                
                # Add delay to respect website limits
                await asyncio.sleep(2)
                
            except Exception as e:
                logger.error(f"Error extracting content from {url}: {e}")
                continue
        
        return content_results
    
    async def _extract_single_url(self, url: str) -> str:
        """Extract content from a single URL (stub)"""
        # In production, this would use Crawl4AI to extract clean content
        try:
            import aiohttp
            
            async with aiohttp.ClientSession() as session:
                async with session.get(url, timeout=30) as response:
                    if response.status == 200:
                        content = await response.text()
                        # Basic HTML cleaning (very basic stub)
                        cleaned_content = self._basic_html_clean(content)
                        logger.debug(f"Extracted {len(cleaned_content)} characters from {url}")
                        return cleaned_content
                    else:
                        logger.warning(f"HTTP {response.status} for {url}")
                        return ""
                        
        except Exception as e:
            logger.error(f"Error extracting {url}: {e}")
            return ""
    
    def _basic_html_clean(self, html_content: str) -> str:
        """Basic HTML cleaning (stub implementation)"""
        # In production, Crawl4AI would handle this properly
        # This is a very basic implementation
        import re
        
        # Remove scripts and styles
        content = re.sub(r'<script.*?</script>', '', html_content, flags=re.DOTALL | re.IGNORECASE)
        content = re.sub(r'<style.*?</style>', '', content, flags=re.DOTALL | re.IGNORECASE)
        
        # Remove HTML tags
        content = re.sub(r'<[^>]+>', ' ', content)
        
        # Clean up whitespace
        content = re.sub(r'\s+', ' ', content)
        content = content.strip()
        
        return content

class CrawlerService:
    """Main crawler service orchestrating URL discovery and content extraction"""
    
    def __init__(self):
        self.tavily = TavilyDiscovery()
        self.extractor = Crawl4AIExtractor()
    
    async def discover_and_crawl(self, insurer_search_terms: Dict[str, List[str]]) -> Dict[str, Dict[str, str]]:
        """Discover URLs and extract content for all insurers"""
        all_results = {}
        
        for insurer, search_terms in insurer_search_terms.items():
            logger.info(f"Processing {insurer}...")
            
            try:
                # Discover URLs
                urls = self.tavily.discover_urls(search_terms, max_results=3)
                
                if not urls:
                    logger.warning(f"No URLs discovered for {insurer}")
                    all_results[insurer] = {}
                    continue
                
                # Extract content
                content_results = await self.extractor.extract_content(urls)
                all_results[insurer] = content_results
                
                logger.info(f"Completed {insurer}: {len(content_results)} pages extracted")
                
            except Exception as e:
                logger.error(f"Error processing {insurer}: {e}")
                all_results[insurer] = {}
        
        return all_results
    
    async def crawl_specific_urls(self, urls: List[str]) -> Dict[str, str]:
        """Crawl specific URLs"""
        return await self.extractor.extract_content(urls)
    
    def get_sample_urls(self) -> Dict[str, List[str]]:
        """Get sample URLs for testing (when Tavily is not available)"""
        return {
            "Zurich Malaysia": [
                "https://www.zurich.com.my/en/individuals/motor-insurance",
                "https://www.zurich.com.my/en/individuals/motor-insurance/z-driver"
            ],
            "Etiqa": [
                "https://www.etiqa.com.my/v2/motor",
                "https://www.etiqa.com.my/v2/motor-takaful"
            ],
            "Allianz General Insurance Malaysia": [
                "https://www.allianz.com.my/personal/motor-insurance"
            ]
        }

# Global instance
crawler_service = CrawlerService()
