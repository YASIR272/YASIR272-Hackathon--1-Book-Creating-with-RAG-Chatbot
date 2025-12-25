"""
Session Context Model for RAG Chatbot Integration
Defines the structure for maintaining conversation context between queries
"""

from datetime import datetime, timedelta
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, validator
from .query_history_item import QueryHistoryItem


class SessionContext(BaseModel):
    """
    Model representing the session context for maintaining conversation state
    """
    session_id: str = Field(..., description="Unique identifier for the session")
    start_time: datetime = Field(default_factory=datetime.utcnow, description="When the session started")
    last_activity: datetime = Field(default_factory=datetime.utcnow, description="When the last activity occurred")
    query_history: List[QueryHistoryItem] = Field(default=[], description="History of queries in the session")
    active_context: Optional[Dict[str, Any]] = Field(default=None, description="Current context for the session")
    timeout_minutes: int = Field(default=30, description="Session timeout in minutes")

    @validator('session_id')
    def validate_session_id(cls, v):
        if not v or len(v.strip()) == 0:
            raise ValueError('Session ID must be a valid non-empty identifier')
        return v.strip()

    @validator('timeout_minutes')
    def validate_timeout_minutes(cls, v):
        if v <= 0:
            raise ValueError('Timeout minutes must be greater than 0')
        if v > 1440:  # More than 24 hours
            raise ValueError('Timeout minutes cannot exceed 1440 (24 hours)')
        return v

    @validator('query_history')
    def validate_query_history(cls, v):
        # Validate that all items in the list are valid QueryHistoryItem objects
        for item in v:
            if not isinstance(item, QueryHistoryItem):
                raise ValueError('All history items must be QueryHistoryItem objects')
        return v

    def add_query(self, query_item: QueryHistoryItem):
        """Add a query to the history and update last activity time"""
        self.query_history.append(query_item)
        self.last_activity = datetime.utcnow()

    def update_active_context(self, context: Dict[str, Any]):
        """Update the active context for the session"""
        self.active_context = context
        self.last_activity = datetime.utcnow()

    def is_expired(self) -> bool:
        """Check if the session has expired based on last activity"""
        time_since_last_activity = datetime.utcnow() - self.last_activity
        return time_since_last_activity > timedelta(minutes=self.timeout_minutes)

    def should_cleanup(self) -> bool:
        """Determine if the session should be cleaned up"""
        return self.is_expired()


# Example usage:
# session = SessionContext(
#     session_id="session_123",
#     query_history=[
#         QueryHistoryItem(
#             query_id="query_456",
#             query_text="What is the main concept?",
#             response_id="response_789"
#         )
#     ]
# )