from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from enum import Enum


class QueryScope(str, Enum):
    """Enumeration for query scope options"""
    FULL_BOOK = "full_book"
    SELECTED_TEXT = "selected_text"


class AgentQueryRequest(BaseModel):
    """Request model for agent queries"""
    query: str = Field(..., min_length=1, max_length=1000, description="Natural language query from the user")
    scope: QueryScope = Field(QueryScope.FULL_BOOK, description="Query scope - full book or selected text only")
    scope_filters: Optional[Dict[str, Any]] = Field(None, description="Metadata filters for selected_text scope")
    max_results: int = Field(5, ge=1, le=20, description="Maximum number of results to retrieve")
    min_similarity: float = Field(0.5, ge=0.0, le=1.0, description="Minimum similarity threshold for results")


class SourceReference(BaseModel):
    """Model representing a source reference in the response"""
    content: str = Field(..., description="Content of the retrieved chunk")
    source_url: str = Field(..., description="URL of the source document")
    source_title: str = Field(..., description="Title of the source document")
    similarity_score: float = Field(..., ge=0.0, le=1.0, description="Similarity score of this chunk")
    metadata: Dict[str, Any] = Field(..., description="Additional metadata about the source")
    chunk_id: str = Field(..., description="Unique identifier for this chunk")


class AgentQueryResponse(BaseModel):
    """Response model for agent queries"""
    response: str = Field(..., description="Agent's response to the query")
    sources: List[SourceReference] = Field(..., description="List of sources used in the response")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Overall confidence level")
    query_time: float = Field(..., description="Time taken to process the query in seconds")
    retrieved_chunks_count: int = Field(..., description="Number of chunks retrieved from vector store")


class HealthCheckResponse(BaseModel):
    """Response model for health check endpoint"""
    status: str = Field(..., description="Health status of the service")
    timestamp: str = Field(..., description="Timestamp of the health check")