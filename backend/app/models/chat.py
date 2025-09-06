from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime

class ChatRequest(BaseModel):
    """Request model for chat messages"""
    message: str = Field(..., min_length=1, max_length=1000, description="User's chat message")
    session_id: Optional[str] = Field(None, description="Optional session identifier for conversation continuity")

class ChatResponse(BaseModel):
    """Response model for chat messages"""
    response: str = Field(..., description="AI-generated response")
    session_id: Optional[str] = Field(None, description="Session identifier if provided")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Response timestamp")

class RAGChatRequest(BaseModel):
    """Request model for RAG-enabled chat messages"""
    message: str = Field(..., min_length=1, max_length=1000, description="User's chat message")
    session_id: Optional[str] = Field(None, description="Optional session identifier for conversation continuity")
    namespace: Optional[str] = Field("insurance_knowledge", description="Knowledge base namespace to search")

class SourceDocument(BaseModel):
    """Model for source documents in RAG responses"""
    source: str = Field(..., description="Source of the information")
    category: str = Field(..., description="Category of the information")
    content_preview: str = Field(..., description="Preview of the content")

class RAGChatResponse(BaseModel):
    """Response model for RAG-enabled chat messages"""
    response: str = Field(..., description="AI-generated response with RAG context")
    session_id: Optional[str] = Field(None, description="Session identifier if provided")
    sources: List[SourceDocument] = Field(default_factory=list, description="Source documents used for response")
    rag_used: bool = Field(..., description="Whether RAG was used for this response")
    context_docs: int = Field(..., description="Number of context documents retrieved")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Response timestamp")

class ChatHistory(BaseModel):
    """Model for chat history"""
    session_id: str = Field(..., description="Session identifier")
    messages: list = Field(default_factory=list, description="List of chat messages")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Session creation time")
    updated_at: datetime = Field(default_factory=datetime.utcnow, description="Last message time")

class KnowledgeBaseStats(BaseModel):
    """Model for knowledge base statistics"""
    total_vectors: int = Field(..., description="Total number of vectors in the index")
    namespaces: Dict[str, int] = Field(default_factory=dict, description="Vector counts by namespace")
    dimension: int = Field(..., description="Vector dimension")
    metric: str = Field(..., description="Distance metric used")

