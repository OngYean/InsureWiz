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
        """Embed a list of texts using Google's embedding-001 model"""
        try:
            # Use Google's embedding-001 model for 768 dimensions
            logger.info("Using Google embedding-001 model for 768 dimensions")
            return self._google_embeddings(texts)
            
        except Exception as e:
            logger.error(f"Error generating Google embeddings: {str(e)}")
            # Fallback to improved embeddings if Google API fails
            return self._improved_fallback_embeddings(texts)
    
    def embed_query(self, text: str) -> List[float]:
        """Embed a single query text using Google's embedding-001 model"""
        try:
            # Use Google's embedding-001 model for 768 dimensions
            logger.info("Using Google embedding-001 model for 768 dimensions")
            return self._google_embeddings([text])[0]
            
        except Exception as e:
            logger.error(f"Error generating Google query embedding: {str(e)}")
            # Fallback to improved embedding if Google API fails
            return self._improved_fallback_embeddings([text])[0]
    
    def _improved_fallback_embeddings(self, texts: List[str]) -> List[List[float]]:
        """Improved fallback embedding method using TF-IDF-like approach with word vectors"""
        embeddings = []
        
        # Define semantic categories and their associated dimensions
        semantic_categories = {
            'insurance': list(range(0, 85)),
            'technology': list(range(85, 170)),
            'business': list(range(170, 255)),
            'health': list(range(255, 340)),
            'motor': list(range(340, 425)),
            'property': list(range(425, 510)),
            'life': list(range(510, 595)),
            'claims': list(range(595, 680)),
            'malaysia': list(range(680, 730)),
            'general': list(range(730, 768))
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
            embedding = [0.0] * 768  # Initialize with zeros for 768 dimensions
            
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
    
    def _google_embeddings(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings using Google's embedding-001 model"""
        try:
            embeddings = []
            for text in texts:
                # Use Google's embedding-001 model
                embedding = genai.embed_content(
                    model="models/embedding-001",
                    content=text,
                    task_type="retrieval_document"
                )
                embeddings.append(embedding['embedding'])
            
            logger.info(f"Generated {len(embeddings)} embeddings using Google embedding-001 model")
            return embeddings
            
        except Exception as e:
            logger.error(f"Error generating Google embeddings: {str(e)}")
            raise e
    
    def _fallback_embeddings(self, texts: List[str]) -> List[List[float]]:
        """Original fallback embedding method using simple hash-based approach"""
        embeddings = []
        for text in texts:
            # Create a deterministic hash-based embedding
            text_hash = hashlib.md5(text.encode()).hexdigest()
            seed = int(text_hash[:8], 16)  # Use first 8 characters as seed
            
            random.seed(seed)
            # Use 768 dimensions to match new Pinecone index
            embedding = [random.uniform(-1, 1) for _ in range(768)]
            embeddings.append(embedding)
        
        logger.warning("Using simple fallback embeddings due to Google API failure")
        return embeddings

# Global embedding service instance
embedding_service = EmbeddingService()
