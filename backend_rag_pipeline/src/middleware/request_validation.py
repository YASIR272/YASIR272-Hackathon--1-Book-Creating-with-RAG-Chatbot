"""
Request Validation Middleware for RAG Chatbot API
Handles rate limiting, input sanitization, and request validation
"""

import time
import re
from collections import defaultdict, deque
from fastapi import HTTPException, Request
from datetime import datetime, timedelta


class RateLimiter:
    """
    Simple in-memory rate limiter
    """
    def __init__(self, max_requests: int = 60, window_size: int = 60):
        self.max_requests = max_requests
        self.window_size = window_size
        self.requests = defaultdict(deque)

    def is_allowed(self, identifier: str) -> bool:
        """
        Check if a request from the given identifier is allowed
        """
        now = time.time()
        window_start = now - self.window_size

        # Remove old requests outside the window
        while self.requests[identifier] and self.requests[identifier][0] < window_start:
            self.requests[identifier].popleft()

        # Check if limit is exceeded
        if len(self.requests[identifier]) >= self.max_requests:
            return False

        # Add current request
        self.requests[identifier].append(now)
        return True


def sanitize_input(text: str) -> str:
    """
    Sanitize input text to prevent injection attacks
    """
    if not text:
        return text

    # Remove potentially dangerous characters/sequences
    sanitized = re.sub(r'<script.*?>.*?</script>', '', text, flags=re.IGNORECASE | re.DOTALL)
    sanitized = re.sub(r'javascript:', '', sanitized, flags=re.IGNORECASE)
    sanitized = re.sub(r'vbscript:', '', sanitized, flags=re.IGNORECASE)
    sanitized = sanitized.replace('<script>', '').replace('</script>', '')

    # Remove other potentially harmful patterns
    sanitized = sanitized.replace('\'', '&apos;').replace('"', '&quot;')

    return sanitized.strip()


def validate_and_sanitize_request(request_data: dict) -> dict:
    """
    Validate and sanitize the incoming request data
    """
    if not isinstance(request_data, dict):
        raise HTTPException(status_code=400, detail="Request must be a JSON object")

    # Sanitize query text
    if 'query' in request_data:
        request_data['query'] = sanitize_input(request_data['query'])
        if len(request_data['query']) > 1000:
            raise HTTPException(status_code=400, detail="Query must be less than 1000 characters")

    # Sanitize selected text
    if 'selectedText' in request_data:
        request_data['selectedText'] = sanitize_input(request_data['selectedText'])
        if request_data['selectedText'] and len(request_data['selectedText']) > 5000:
            raise HTTPException(status_code=400, detail="Selected text must be less than 5000 characters")

    # Sanitize session ID
    if 'sessionId' in request_data:
        request_data['sessionId'] = sanitize_input(request_data['sessionId'])
        if not request_data['sessionId']:
            raise HTTPException(status_code=400, detail="Session ID is required")

    return request_data


# Global rate limiter instance
rate_limiter = RateLimiter(max_requests=30, window_size=60)  # 30 requests per minute per IP