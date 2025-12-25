"""
Query History Item Model for RAG Chatbot Integration
Defines the structure for tracking individual query-response pairs in a session
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, validator


class QueryHistoryItem(BaseModel):
    """
    Model representing a single query-response pair in session history
    """
    query_id: str = Field(..., description="Reference to the original query")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="When the query was made")
    query_text: str = Field(..., min_length=1, description="The original query text")
    response_id: Optional[str] = Field(None, description="Reference to the response, if any")

    @validator('query_id', 'query_text')
    def validate_non_empty_fields(cls, v):
        if not v or len(v.strip()) == 0:
            raise ValueError('Query ID and query text must be non-empty')
        return v.strip()

    @validator('query_text')
    def validate_query_text_length(cls, v):
        if len(v) > 1000:
            raise ValueError('Query text must be less than 1000 characters')
        return v


# Example usage:
# history_item = QueryHistoryItem(
#     query_id="query_123",
#     query_text="What is the main concept?",
#     response_id="response_456"
# )