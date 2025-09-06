import os
import sys
from typing import List, Dict, Any
from pathlib import Path
import markdown
from bs4 import BeautifulSoup
from langchain.schema import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from app.services.vector_store import vector_store_service
from app.utils.logger import setup_logger
from app.utils.exceptions import VectorStoreException

logger = setup_logger("project_document_service")

class ProjectDocumentService:
    """Service for ingesting and managing project documentation in the vector store"""
    
    def __init__(self):
        self.vector_store = vector_store_service
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
            separators=["\n\n", "\n", " ", ""]
        )
        
        # Project documentation files to ingest
        self.project_docs = [
            "README.md",
            "PROJECT_OVERVIEW.md",
            "TECHNICAL_ARCHITECTURE.md",
            "AI_INTEGRATION_GUIDE.md",
            "DEVELOPMENT_GUIDE.md",
            "API_REFERENCE.md",
            "DOCUMENTATION_INDEX.md",
            "INSUREWIZ_COMPREHENSIVE_GUIDE.md",
            "INSUREWIZ_TECHNICAL_FEATURES.md",
            "INSUREWIZ_BUSINESS_MODEL.md"
        ]
    
    def ingest_project_documentation(self, namespace: str = "project_knowledge") -> bool:
        """Ingest all project documentation into the vector store"""
        try:
            logger.info("Starting project documentation ingestion...")
            
            # Get the project root directory (parent of backend)
            project_root = Path(__file__).parent.parent.parent
            logger.info(f"Project root directory: {project_root}")
            
            documents = []
            
            for doc_file in self.project_docs:
                doc_path = project_root / doc_file
                
                if doc_path.exists():
                    logger.info(f"Processing document: {doc_file}")
                    
                    # Read and process the markdown file
                    doc_content = self._process_markdown_file(doc_path)
                    
                    if doc_content:
                        # Create document chunks
                        chunks = self.text_splitter.split_text(doc_content)
                        
                        # Create Document objects for each chunk
                        for i, chunk in enumerate(chunks):
                            doc = Document(
                                page_content=chunk.strip(),
                                metadata={
                                    "source": doc_file,
                                    "category": "project_documentation",
                                    "language": "english",
                                    "chunk_index": i,
                                    "total_chunks": len(chunks),
                                    "file_type": "markdown"
                                }
                            )
                            documents.append(doc)
                        
                        logger.info(f"Created {len(chunks)} chunks from {doc_file}")
                    else:
                        logger.warning(f"Failed to process {doc_file}")
                else:
                    logger.warning(f"Document file not found: {doc_file}")
            
            if not documents:
                logger.error("No documents were processed successfully")
                return False
            
            # Add documents to vector store
            success = self.vector_store.add_documents(
                documents=documents,
                namespace=namespace
            )
            
            if success:
                logger.info(f"Successfully ingested {len(documents)} project documentation chunks")
                return True
            else:
                logger.error("Failed to add project documents to vector store")
                return False
                
        except Exception as e:
            logger.error(f"Error ingesting project documentation: {str(e)}")
            raise VectorStoreException(
                message="Failed to ingest project documentation",
                details={"error": str(e)}
            )
    
    def _process_markdown_file(self, file_path: Path) -> str:
        """Process a markdown file and extract clean text content"""
        try:
            # Read the markdown file
            with open(file_path, 'r', encoding='utf-8') as f:
                markdown_content = f.read()
            
            # Convert markdown to HTML
            html_content = markdown.markdown(markdown_content)
            
            # Parse HTML and extract text
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # Remove code blocks (they can be noisy for embeddings)
            for code_block in soup.find_all(['code', 'pre']):
                code_block.decompose()
            
            # Extract clean text
            clean_text = soup.get_text()
            
            # Clean up whitespace
            clean_text = ' '.join(clean_text.split())
            
            return clean_text
            
        except Exception as e:
            logger.error(f"Error processing markdown file {file_path}: {str(e)}")
            return ""
    
    def search_project_knowledge(self, query: str, namespace: str = "project_knowledge") -> List[Document]:
        """Search project documentation for relevant information"""
        try:
            results = self.vector_store.similarity_search(
                query=query,
                namespace=namespace
            )
            
            logger.info(f"Found {len(results)} relevant project documents for query: {query[:50]}...")
            return results
            
        except Exception as e:
            logger.error(f"Error searching project knowledge: {str(e)}")
            raise VectorStoreException(
                message="Failed to search project knowledge",
                details={"error": str(e)}
            )
    
    def get_project_docs_stats(self, namespace: str = "project_knowledge") -> Dict[str, Any]:
        """Get statistics about project documentation in the vector store"""
        try:
            stats = self.vector_store.get_index_stats()
            
            # Filter for project knowledge namespace
            project_stats = {
                "total_vectors": stats.get("total_vector_count", 0),
                "namespaces": stats.get("namespaces", {}),
                "project_namespace": stats.get("namespaces", {}).get(namespace, {}),
                "index_dimension": stats.get("dimension", 0),
                "index_metric": stats.get("metric", "unknown")
            }
            
            return project_stats
            
        except Exception as e:
            logger.error(f"Error getting project docs stats: {str(e)}")
            raise VectorStoreException(
                message="Failed to get project documentation statistics",
                details={"error": str(e)}
            )
    
    def add_custom_project_document(self, file_path: str, namespace: str = "project_knowledge") -> bool:
        """Add a custom project document to the vector store"""
        try:
            doc_path = Path(file_path)
            
            if not doc_path.exists():
                logger.error(f"File not found: {file_path}")
                return False
            
            # Process the document
            doc_content = self._process_markdown_file(doc_path)
            
            if not doc_content:
                logger.error(f"Failed to process document: {file_path}")
                return False
            
            # Create chunks
            chunks = self.text_splitter.split_text(doc_content)
            
            # Create Document objects
            documents = []
            for i, chunk in enumerate(chunks):
                doc = Document(
                    page_content=chunk.strip(),
                    metadata={
                        "source": doc_path.name,
                        "category": "custom_project_document",
                        "language": "english",
                        "chunk_index": i,
                        "total_chunks": len(chunks),
                        "file_type": "markdown",
                        "custom": True
                    }
                )
                documents.append(doc)
            
            # Add to vector store
            success = self.vector_store.add_documents(
                documents=documents,
                namespace=namespace
            )
            
            if success:
                logger.info(f"Successfully added custom project document: {file_path}")
                return True
            else:
                logger.error(f"Failed to add custom project document: {file_path}")
                return False
                
        except Exception as e:
            logger.error(f"Error adding custom project document: {str(e)}")
            raise VectorStoreException(
                message="Failed to add custom project document",
                details={"error": str(e)}
            )

# Global project document service instance
project_document_service = ProjectDocumentService()

