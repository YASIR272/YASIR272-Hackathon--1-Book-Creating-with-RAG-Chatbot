"""
RAG Response Model for RAG Chatbot Integration
Defines the structure for responses from the RAG system
"""

from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field, validator
from .source_reference import SourceReference


class RAGResponse(BaseModel):
    """
    Model representing a response from the RAG system
    """
    id: str = Field(..., description="Unique identifier for the response")
    query_id: str = Field(..., description="Reference to the original query")
    answer: str = Field(..., min_length=1, description="The generated answer from the RAG system")
    sources: List[SourceReference] = Field(default=[], description="Citations to book content")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="When the response was generated")
    session_id: str = Field(..., description="Session identifier for maintaining conversation context")

    @validator('answer')
    def validate_answer(cls, v):
        if not v or len(v.strip()) == 0:
            raise ValueError('Answer must be non-empty')
        return v.strip()

    @validator('sources')
    def validate_sources(cls, v):
        # Validate that all items in the list are valid SourceReference objects
        for source in v:
            if not isinstance(source, SourceReference):
                raise ValueError('All sources must be SourceReference objects')
        return v

    @validator('query_id', 'session_id')
    def validate_identifiers(cls, v):
        if not v or len(v.strip()) == 0:
            raise ValueError('Identifiers must be valid non-empty strings')
        return v.strip()


# Example usage:
# response = RAGResponse(
#     id="response_123",
#     query_id="query_456",
#     answer="The main concept discussed is...",
#     sources=[
#         SourceReference(
#             document_id="doc_789",
#             section="Chapter 1: Introduction",
#             page_url="/docs/intro",
#             text="The main concept is...",
#             confidence=0.95
#         )
#     ],
#     session_id="session_101"
# )