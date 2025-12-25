"""
API Communication Layer Model for RAG Chatbot Integration
Defines the structure for tracking API requests and responses
"""

from datetime import datetime
from typing import Any, Optional
from pydantic import BaseModel, Field, validator


class APICommunication(BaseModel):
    """
    Model representing an API communication event for logging and monitoring
    """
    request_id: str = Field(..., description="Unique identifier for the API request")
    endpoint: str = Field(..., description="The API endpoint being called")
    method: str = Field(..., description="HTTP method: GET, POST, etc.")
    request_payload: Any = Field(..., description="The data sent in the request")
    response_payload: Any = Field(..., description="The data received in response")
    status: int = Field(..., ge=100, le=599, description="HTTP status code")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="When the request was made")
    duration: float = Field(..., ge=0, description="Time taken for the request in milliseconds")

    @validator('endpoint', 'method')
    def validate_non_empty_fields(cls, v):
        if not v or len(v.strip()) == 0:
            raise ValueError('Endpoint and method must be non-empty')
        return v.strip()

    @validator('method')
    def validate_http_method(cls, v):
        valid_methods = ['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'HEAD', 'OPTIONS']
        if v.upper() not in valid_methods:
            raise ValueError(f'Method must be one of {valid_methods}')
        return v.upper()

    @validator('status')
    def validate_status_code(cls, v):
        if v < 100 or v > 599:
            raise ValueError('Status code must be between 100 and 599')
        return v


# Example usage:
# communication = APICommunication(
#     request_id="req_123",
#     endpoint="/api/v1/chat/query",
#     method="POST",
#     request_payload={"query": "What is this?", "selectedText": "", "sessionId": "session_456"},
#     response_payload={"id": "resp_789", "answer": "This is the answer"},
#     status=200,
#     duration=150.5
# )