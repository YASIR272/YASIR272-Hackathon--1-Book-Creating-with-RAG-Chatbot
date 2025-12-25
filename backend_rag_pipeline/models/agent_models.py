from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from datetime import datetime


class RetrievedChunk(BaseModel):
    """
    Represents a chunk of content retrieved from the vector store
    """
    id: str
    content: str
    similarity_score: float
    source_url: str
    source_title: str
    metadata: Dict[str, Any]
    vector_embedding: Optional[List[float]] = None


class AgentQuery(BaseModel):
    """
    Internal model representing a query being processed by the agent
    """
    query_text: str
    scope_filters: Optional[Dict[str, Any]] = None
    retrieved_context: List[RetrievedChunk]
    agent_response: str
    processed_response: str
    execution_time: float
    timestamp: datetime = datetime.now()


class ScopedQueryRequest(BaseModel):
    """
    Model for queries with scope filters
    """
    query_text: str
    scope: str = "full_book"  # "full_book" or "selected_text"
    scope_filters: Optional[Dict[str, Any]] = None
    max_results: int = 5
    min_similarity: float = 0.5


class SourceReference(BaseModel):
    """
    Model representing a source reference in the response
    """
    content: str
    source_url: str
    source_title: str
    similarity_score: float
    metadata: Dict[str, Any]
    chunk_id: str