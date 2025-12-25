from typing import List, Dict, Optional
from pydantic import BaseModel
from dataclasses import dataclass
from typing import Union


class MetadataFilter(BaseModel):
    """Criteria used to filter search results by metadata attributes"""
    field_name: str
    operator: str
    value: Union[str, List[str]]
    case_sensitive: bool = False


class QueryRequest(BaseModel):
    """Represents a user query with optional metadata filters"""
    query_text: str
    metadata_filters: Optional[Dict[str, str]] = None
    top_k: int = 5
    similarity_threshold: Optional[float] = None


class RetrievedChunk(BaseModel):
    """A text chunk retrieved from the vector database"""
    content: str
    similarity_score: float
    source_url: str
    source_title: str
    metadata: Dict[str, str]
    confidence_score: float


class RetrievalResult(BaseModel):
    """The complete result of a retrieval operation"""
    query_request: QueryRequest
    retrieved_chunks: List[RetrievedChunk]
    execution_time: float
    total_chunks_found: int
    search_params: Dict[str, str]


class ValidationResult(BaseModel):
    """Result of a validation test against expected answers"""
    query: str
    expected_answers: List[str]
    retrieved_chunks: List[RetrievedChunk]
    accuracy_score: float
    validation_passed: bool
    detailed_feedback: Optional[str] = None