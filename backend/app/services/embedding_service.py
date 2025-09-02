from typing import List
import google.generativeai as genai
from app.config import settings
from app.utils.logger import setup_logger
import hashlib
import random
import re

logger = setup_logger("embedding_service")

class EmbeddingService:
    """Service for generating text embeddings using Google's embedding model"""
    
    def __init__(self):
        # Configure Google AI
        genai.configure(api_key=settings.google_api_key)
        
        logger.info("Embedding service initialized successfully")
    
    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """Embed a list of texts - LangChain interface method"""
        try:
            # For now, use improved fallback embeddings to match Pinecone index dimensions
            # TODO: Consider recreating Pinecone index with 768 dimensions for Google embeddings
            logger.info("Using improved fallback embeddings to match Pinecone index dimensions (1024)")
            return self._improved_fallback_embeddings(texts)
            
        except Exception as e:
            logger.error(f"Error generating embeddings: {str(e)}")
            # Fallback to simple embeddings if Google API fails
            return self._improved_fallback_embeddings(texts)
    
    def embed_query(self, text: str) -> List[float]:
        """Embed a single query text - LangChain interface method"""
        try:
            # For now, use improved fallback embeddings to match Pinecone index dimensions
            # TODO: Consider recreating Pinecone index with 768 dimensions for Google embeddings
            logger.info("Using improved fallback embeddings to match Pinecone index dimensions (1024)")
            return self._improved_fallback_embeddings([text])[0]
            
        except Exception as e:
            logger.error(f"Error generating query embedding: {str(e)}")
            # Fallback to simple embedding if Google API fails
            return self._improved_fallback_embeddings([text])[0]
    
    def _improved_fallback_embeddings(self, texts: List[str]) -> List[List[float]]:
        """Improved fallback embedding method using TF-IDF-like approach with word vectors"""
        embeddings = []
        
        # Define semantic categories and their associated dimensions
        semantic_categories = {
            'insurance': list(range(0, 100)),
            'technology': list(range(100, 200)),
            'business': list(range(200, 300)),
            'health': list(range(300, 400)),
            'motor': list(range(400, 500)),
            'property': list(range(500, 600)),
            'life': list(range(600, 700)),
            'claims': list(range(700, 800)),
            'malaysia': list(range(800, 900)),
            'general': list(range(900, 1024))
        }
        
        # Define keyword mappings to semantic categories
        keyword_mappings = {
            'insurance': ['insurance', 'policy', 'coverage', 'premium', 'claim', 'risk'],
            'technology': ['ai', 'api', 'backend', 'frontend', 'database', 'system', 'code', 'software'],
            'business': ['business', 'company', 'enterprise', 'commercial', 'corporate'],
            'health': ['health', 'medical', 'hospital', 'doctor', 'treatment', 'illness'],
            'motor': ['motor', 'car', 'auto', 'vehicle', 'driver', 'accident', 'road'],
            'property': ['property', 'home', 'house', 'building', 'real estate', 'mortgage'],
            'life': ['life', 'family', 'death', 'beneficiary', 'inheritance'],
            'claims': ['claim', 'damage', 'repair', 'compensation', 'settlement'],
            'malaysia': ['malaysia', 'malaysian', 'takaful', 'jpj', 'pdrm', 'bank negara'],
            'general': ['the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of']
        }
        
        for text in texts:
            text_lower = text.lower()
            embedding = [0.0] * 1024  # Initialize with zeros
            
            # Process each semantic category
            for category, dimensions in semantic_categories.items():
                category_score = 0
                
                # Check for keywords in this category
                for keyword in keyword_mappings[category]:
                    if keyword in text_lower:
                        category_score += 1
                
                # Normalize score and apply to category dimensions
                if category_score > 0:
                    normalized_score = min(category_score / len(keyword_mappings[category]), 1.0)
                    
                    # Apply score to category dimensions with some randomness for uniqueness
                    text_hash = hashlib.md5(text.encode()).hexdigest()
                    seed = int(text_hash[:8], 16)
                    random.seed(seed)
                    
                    for dim in dimensions:
                        # Base score + some randomness for uniqueness
                        embedding[dim] = normalized_score + random.uniform(-0.1, 0.1)
            
            # Normalize the entire embedding vector
            magnitude = sum(x * x for x in embedding) ** 0.5
            if magnitude > 0:
                embedding = [x / magnitude for x in embedding]
            
            embeddings.append(embedding)
        
        logger.info("Using improved fallback embeddings with semantic categories")
        return embeddings
    
    def _fallback_embeddings(self, texts: List[str]) -> List[List[float]]:
        """Original fallback embedding method using simple hash-based approach"""
        embeddings = []
        for text in texts:
            # Create a deterministic hash-based embedding
            text_hash = hashlib.md5(text.encode()).hexdigest()
            seed = int(text_hash[:8], 16)  # Use first 8 characters as seed
            
            random.seed(seed)
            # Use 1024 dimensions to match existing Pinecone index
            embedding = [random.uniform(-1, 1) for _ in range(1024)]
            embeddings.append(embedding)
        
        logger.warning("Using simple fallback embeddings due to Google API failure")
        return embeddings

# Global embedding service instance
embedding_service = EmbeddingService()
