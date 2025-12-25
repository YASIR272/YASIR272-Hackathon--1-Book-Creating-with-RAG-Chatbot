"""
Source Reference Model for RAG Chatbot Integration
Defines the structure for source citations in RAG responses
"""

from typing import Optional
from pydantic import BaseModel, Field, validator


class SourceReference(BaseModel):
    """
    Model representing a source reference/citation in RAG responses
    """
    document_id: str = Field(..., description="Identifier for the source document")
    section: str = Field(..., description="Section title or heading")
    page_url: str = Field(..., description="URL to the page containing the source")
    text: str = Field(..., min_length=1, description="The actual text that was referenced")
    confidence: Optional[float] = Field(0.0, ge=0.0, le=1.0, description="Confidence score of the reference (0-1)")

    @validator('document_id', 'section', 'page_url', 'text')
    def validate_non_empty_fields(cls, v):
        if not v or len(v.strip()) == 0:
            raise ValueError('All fields must be non-empty')
        return v.strip()

    @validator('confidence')
    def validate_confidence(cls, v):
        if v is not None and (v < 0.0 or v > 1.0):
            raise ValueError('Confidence must be between 0 and 1')
        return v


# Example usage:
# source = SourceReference(
#     document_id="doc_123",
#     section="Chapter 1: Introduction",
#     page_url="/docs/intro",
#     text="The main concept is...",
#     confidence=0.95
# )