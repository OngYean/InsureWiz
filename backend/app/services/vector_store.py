from typing import List, Dict, Any, Optional
import pinecone
from langchain_pinecone import PineconeVectorStore
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.schema import Document
from app.config import settings
from app.utils.logger import setup_logger
from app.utils.exceptions import VectorStoreException
from app.services.embedding_service import embedding_service

logger = setup_logger("vector_store")

class VectorStoreService:
    """Service for managing Pinecone vector store operations"""
    
    def __init__(self):
        self.pinecone_api_key = settings.pinecone_api_key
        self.pinecone_environment = settings.pinecone_environment
        self.index_name = settings.pinecone_index_name
        self.chunk_size = settings.chunk_size
        self.chunk_overlap = settings.chunk_overlap
        self.top_k = settings.top_k_results
        
        # Initialize Pinecone
        self._initialize_pinecone()
        
        # Initialize text splitter
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            length_function=len,
            separators=["\n\n", "\n", " ", ""]
        )
    
    def _initialize_pinecone(self):
        """Initialize Pinecone client and create index if it doesn't exist"""
        try:
            # Use new Pinecone class-based approach
            self.pc = pinecone.Pinecone(api_key=self.pinecone_api_key)
            
            # Check if index exists, create if it doesn't
            if self.index_name not in self.pc.list_indexes().names():
                logger.info(f"Creating Pinecone index: {self.index_name}")
                self.pc.create_index(
                    name=self.index_name,
                    dimension=768,  # Use 768 to match embedding-001 model
                    metric="cosine"
                )
                logger.info(f"Pinecone index '{self.index_name}' created successfully")
            else:
                logger.info(f"Pinecone index '{self.index_name}' already exists")
                
        except Exception as e:
            logger.error(f"Error initializing Pinecone: {str(e)}")
            raise VectorStoreException(
                message="Failed to initialize Pinecone",
                details={"error": str(e)}
            )
    
    def add_documents(self, documents: List[Document], namespace: str = "default") -> bool:
        """Add documents to the vector store"""
        try:
            # Split documents into chunks
            chunks = self.text_splitter.split_documents(documents)
            logger.info(f"Split {len(documents)} documents into {len(chunks)} chunks")
            
            # Use the proper embedding service
            vectorstore = PineconeVectorStore.from_documents(
                documents=chunks,
                embedding=embedding_service,
                index_name=self.index_name,
                namespace=namespace
            )
            
            logger.info(f"Successfully added {len(chunks)} chunks to vector store")
            return True
            
        except Exception as e:
            logger.error(f"Error adding documents to vector store: {str(e)}")
            raise VectorStoreException(
                message="Failed to add documents to vector store",
                details={"error": str(e)}
            )
    
    def add_texts(self, texts: List[str], metadatas: Optional[List[Dict[str, Any]]] = None, 
                  namespace: str = "default") -> bool:
        """Add raw texts to the vector store"""
        try:
            # Create documents from texts
            if metadatas is None:
                metadatas = [{"source": "user_input"} for _ in texts]
            
            documents = [
                Document(page_content=text, metadata=metadata)
                for text, metadata in zip(texts, metadatas)
            ]
            
            return self.add_documents(documents, namespace)
            
        except Exception as e:
            logger.error(f"Error adding texts to vector store: {str(e)}")
            raise VectorStoreException(
                message="Failed to add texts to vector store",
                details={"error": str(e)}
            )
    
    def similarity_search(self, query: str, namespace: str = "default") -> List[Document]:
        """Search for similar documents in the vector store"""
        try:
            # Create a custom embedding class that matches the expected interface
            class CustomEmbedding:
                def __init__(self, embedding_service):
                    self.embedding_service = embedding_service
                
                def embed_documents(self, texts):
                    return self.embedding_service.embed_documents(texts)
                
                def embed_query(self, text):
                    return self.embedding_service.embed_query(text)
            
            custom_embedding = CustomEmbedding(embedding_service)
            
            vectorstore = PineconeVectorStore.from_existing_index(
                index_name=self.index_name,
                embedding=custom_embedding,
                namespace=namespace
            )
            
            # Perform similarity search with more lenient parameters
            # Use a higher k value and lower similarity threshold to get more results
            results = vectorstore.similarity_search_with_score(
                query=query,
                k=self.top_k * 2,  # Get more results initially
                namespace=namespace
            )
            
            # Filter results by a reasonable similarity threshold
            # Since we're using custom embeddings, we'll be more lenient
            filtered_results = []
            for doc, score in results:
                # Convert distance to similarity (cosine distance to similarity)
                # Lower distance = higher similarity
                similarity = 1 - score  # Convert distance to similarity
                
                # Use a lower threshold for custom embeddings
                if similarity > 0.1:  # Very lenient threshold
                    filtered_results.append(doc)
                
                # Limit to top_k results
                if len(filtered_results) >= self.top_k:
                    break
            
            logger.info(f"Found {len(filtered_results)} similar documents for query: {query[:50]}...")
            return filtered_results
            
        except Exception as e:
            logger.error(f"Error performing similarity search: {str(e)}")
            # Fallback: try to get any documents from the namespace
            try:
                # Get a few random documents as fallback
                index = self.pc.Index(self.index_name)
                stats = index.describe_index_stats()
                
                if namespace and namespace in stats.get('namespaces', {}):
                    # Return some documents from the namespace as fallback
                    logger.info(f"Using fallback document retrieval for namespace: {namespace}")
                    # For now, return empty list - the AI service will handle fallback
                    return []
                else:
                    return []
                    
            except Exception as fallback_error:
                logger.error(f"Fallback document retrieval also failed: {str(fallback_error)}")
                return []
    
    def delete_namespace(self, namespace: str) -> bool:
        """Delete all vectors in a specific namespace"""
        try:
            index = self.pc.Index(self.index_name)
            index.delete(namespace=namespace)
            logger.info(f"Successfully deleted namespace: {namespace}")
            return True
            
        except Exception as e:
            logger.error(f"Error deleting namespace: {str(e)}")
            raise VectorStoreException(
                message="Failed to delete namespace",
                details={"error": str(e)}
            )
    
    def get_index_stats(self) -> Dict[str, Any]:
        """Get statistics about the vector store index"""
        try:
            index = self.pc.Index(self.index_name)
            stats = index.describe_index_stats()
            logger.info(f"Retrieved index statistics: {stats}")
            return stats
            
        except Exception as e:
            logger.error(f"Error getting index statistics: {str(e)}")
            raise VectorStoreException(
                message="Failed to get index statistics",
                details={"error": str(e)}
            )

# Global vector store service instance
vector_store_service = VectorStoreService()
