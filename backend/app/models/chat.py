from pydantic import BaseModel, Field
from typing import Optional
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

class ChatHistory(BaseModel):
    """Model for chat history"""
    session_id: str = Field(..., description="Session identifier")
    messages: list = Field(default_factory=list, description="List of chat messages")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Session creation time")
    updated_at: datetime = Field(default_factory=datetime.utcnow, description="Last message time")

