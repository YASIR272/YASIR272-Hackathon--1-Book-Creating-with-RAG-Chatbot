"""
Logging Utility for RAG Chatbot API
Provides structured logging for API requests and responses
"""

import logging
import json
from datetime import datetime
from typing import Any, Dict
from ..models.api_communication import APICommunication


class APILogger:
    """
    Structured logger for API communications
    """
    def __init__(self, name: str = "rag_chatbot_api"):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)

        # Create console handler if not already exists
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)

    def log_request(self, request_id: str, endpoint: str, method: str, payload: Any):
        """
        Log an incoming API request
        """
        log_data = {
            "type": "api_request",
            "request_id": request_id,
            "endpoint": endpoint,
            "method": method,
            "timestamp": datetime.utcnow().isoformat(),
            "payload": payload
        }
        self.logger.info(json.dumps(log_data))

    def log_response(self, request_id: str, status: int, payload: Any, duration: float):
        """
        Log an API response
        """
        log_data = {
            "type": "api_response",
            "request_id": request_id,
            "status": status,
            "duration_ms": duration,
            "timestamp": datetime.utcnow().isoformat(),
            "payload": payload
        }
        self.logger.info(json.dumps(log_data))

    def log_error(self, request_id: str, endpoint: str, error: str, details: Dict[str, Any] = None):
        """
        Log an API error
        """
        log_data = {
            "type": "api_error",
            "request_id": request_id,
            "endpoint": endpoint,
            "error": error,
            "timestamp": datetime.utcnow().isoformat(),
            "details": details or {}
        }
        self.logger.error(json.dumps(log_data))


# Global logger instance
api_logger = APILogger()