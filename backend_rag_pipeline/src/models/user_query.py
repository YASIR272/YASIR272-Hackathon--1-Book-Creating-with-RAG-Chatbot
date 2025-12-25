"""
User Query Model for RAG Chatbot Integration
Defines the structure for user queries to the RAG system
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, validator


class UserQuery(BaseModel):
    """
    Model representing a user query to the RAG system
    """
    id: str = Field(..., description="Unique identifier for the query")
    text: str = Field(..., min_length=1, max_length=1000, description="The actual query text from the user")
    selected_text: Optional[str] = Field(None, max_length=5000, description="Optional selected text context")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="When the query was submitted")
    session_id: str = Field(..., description="Session identifier for maintaining conversation context")

    @validator('text')
    def validate_query_text(cls, v):
        if not v or len(v.strip()) == 0:
            raise ValueError('Query text must be non-empty')
        if len(v) > 1000:
            raise ValueError('Query text must be less than 1000 characters')
        return v.strip()

    @validator('selected_text')
    def validate_selected_text(cls, v):
        if v and len(v) > 5000:
            raise ValueError('Selected text must be less than 5000 characters')
        return v

    @validator('session_id')
    def validate_session_id(cls, v):
        if not v or len(v.strip()) == 0:
            raise ValueError('Session ID must be a valid identifier')
        return v.strip()


# Example usage:
# query = UserQuery(
#     id="query_123",
#     text="What is the main concept discussed in this section?",
#     selected_text="Optional selected text that provides context for the query",
#     session_id="session_456"
# )