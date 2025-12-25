"""
Chat API Endpoints for RAG Chatbot Integration
"""

from fastapi import APIRouter, HTTPException, BackgroundTasks, Request
from datetime import datetime
import uuid
import time
from typing import Dict, Any, Optional
from pydantic import BaseModel
from ...models.user_query import UserQuery
from ...models.rag_response import RAGResponse
from ...models.source_reference import SourceReference
from ...models.session_context import SessionContext
from ...models.query_history_item import QueryHistoryItem
from ...services.query_processor import QueryProcessor
from ...middleware.request_validation import rate_limiter, validate_and_sanitize_request
from ...utils.logger import api_logger
from ...utils.session_cleanup import init_cleanup_manager


# Create router
router = APIRouter()

# In-memory storage for sessions (in production, use a proper database)
sessions: Dict[str, SessionContext] = {}

# Initialize cleanup manager
cleanup_manager = init_cleanup_manager(sessions)

# Initialize query processor
query_processor = QueryProcessor()

# Start the cleanup task when the module is loaded
import asyncio
try:
    # This will run the cleanup manager in the background
    if hasattr(asyncio, 'create_task'):
        cleanup_task = asyncio.create_task(cleanup_manager.start_cleanup_task())
except:
    # Fallback for different asyncio implementations
    pass


class QueryRequest(BaseModel):
    query: str
    selectedText: Optional[str] = ""
    sessionId: str


class ValidateRequest(BaseModel):
    pass  # No body needed for validation


@router.post("/chat/query", response_model=RAGResponse)
async def submit_query(request: QueryRequest, fastapi_request: Request):
    """
    Submit a user query to the RAG system with optional selected text context
    """
    start_time = time.time()
    request_id = f"req_{uuid.uuid4().hex[:8]}"

    try:
        # Log the incoming request
        api_logger.log_request(
            request_id=request_id,
            endpoint="/chat/query",
            method="POST",
            payload={"query_length": len(request.query), "has_selected_text": bool(request.selectedText), "sessionId": request.sessionId}
        )

        # Rate limiting
        client_ip = fastapi_request.client.host
        if not rate_limiter.is_allowed(client_ip):
            api_logger.log_error(
                request_id=request_id,
                endpoint="/chat/query",
                error="Rate limit exceeded",
                details={"client_ip": client_ip}
            )
            raise HTTPException(status_code=429, detail="Rate limit exceeded. Please try again later.")

        # Sanitize and validate request data
        sanitized_request = {
            "query": request.query,
            "selectedText": request.selectedText,
            "sessionId": request.sessionId
        }
        sanitized_request = validate_and_sanitize_request(sanitized_request)

        # Validate the request using the UserQuery model validation
        user_query = UserQuery(
            id=f"query_{uuid.uuid4().hex[:8]}",
            text=sanitized_request["query"],
            selected_text=sanitized_request["selectedText"] or None,
            session_id=sanitized_request["sessionId"]
        )

        # Get or create session context
        if user_query.session_id not in sessions:
            sessions[user_query.session_id] = SessionContext(
                session_id=user_query.session_id
            )

        session = sessions[user_query.session_id]

        # Process the query using the query processor
        response_text, sources = await query_processor.process_query(
            user_query.text,
            user_query.selected_text
        )

        # Generate a unique response ID
        response_id = f"response_{uuid.uuid4().hex[:8]}"

        # Create the RAG response
        rag_response = RAGResponse(
            id=response_id,
            query_id=user_query.id,
            answer=response_text,
            sources=sources,
            session_id=user_query.session_id
        )

        # Add query to session history
        history_item = QueryHistoryItem(
            query_id=user_query.id,
            query_text=user_query.text,
            response_id=rag_response.id
        )
        session.add_query(history_item)

        # Calculate duration
        duration = (time.time() - start_time) * 1000  # Convert to milliseconds

        # Log the successful response
        api_logger.log_response(
            request_id=request_id,
            status=200,
            payload={"response_id": response_id, "answer_length": len(response_text), "source_count": len(sources)},
            duration=duration
        )

        return rag_response

    except HTTPException as e:
        duration = (time.time() - start_time) * 1000  # Convert to milliseconds
        api_logger.log_error(
            request_id=request_id,
            endpoint="/chat/query",
            error=f"HTTP {e.status_code}: {e.detail}",
            details={"status_code": e.status_code}
        )
        raise
    except Exception as e:
        duration = (time.time() - start_time) * 1000  # Convert to milliseconds
        api_logger.log_error(
            request_id=request_id,
            endpoint="/chat/query",
            error=f"Internal server error: {str(e)}",
            details={"exception_type": type(e).__name__}
        )
        raise HTTPException(status_code=500, detail=f"Error processing query: {str(e)}")


@router.get("/chat/session/{sessionId}")
async def get_session(sessionId: str):
    """
    Retrieve session information and query history
    """
    start_time = time.time()
    request_id = f"req_{uuid.uuid4().hex[:8]}"

    try:
        # Log the incoming request
        api_logger.log_request(
            request_id=request_id,
            endpoint=f"/chat/session/{sessionId}",
            method="GET",
            payload={"sessionId": sessionId}
        )

        if sessionId not in sessions:
            api_logger.log_error(
                request_id=request_id,
                endpoint=f"/chat/session/{sessionId}",
                error="Session not found",
                details={"sessionId": sessionId}
            )
            raise HTTPException(status_code=404, detail="Session not found")

        session = sessions[sessionId]
        response_data = {
            "sessionId": session.session_id,
            "startTime": session.start_time.isoformat(),
            "lastActivity": session.last_activity.isoformat(),
            "queryHistory": [
                {
                    "queryId": item.query_id,
                    "timestamp": item.timestamp.isoformat(),
                    "queryText": item.query_text,
                    "responseId": item.response_id
                }
                for item in session.query_history
            ],
            "activeContext": session.active_context
        }

        # Calculate duration
        duration = (time.time() - start_time) * 1000  # Convert to milliseconds

        # Log the successful response
        api_logger.log_response(
            request_id=request_id,
            status=200,
            payload={"query_history_count": len(session.query_history)},
            duration=duration
        )

        return response_data
    except HTTPException as e:
        duration = (time.time() - start_time) * 1000  # Convert to milliseconds
        api_logger.log_error(
            request_id=request_id,
            endpoint=f"/chat/session/{sessionId}",
            error=f"HTTP {e.status_code}: {e.detail}",
            details={"status_code": e.status_code}
        )
        raise
    except Exception as e:
        duration = (time.time() - start_time) * 1000  # Convert to milliseconds
        api_logger.log_error(
            request_id=request_id,
            endpoint=f"/chat/session/{sessionId}",
            error=f"Internal server error: {str(e)}",
            details={"exception_type": type(e).__name__}
        )
        raise HTTPException(status_code=500, detail=f"Error retrieving session: {str(e)}")


@router.post("/chat/validate")
async def validate_connection(fastapi_request: Request):
    """
    Validate the connection to the RAG backend service
    """
    start_time = time.time()
    request_id = f"req_{uuid.uuid4().hex[:8]}"

    try:
        # Log the incoming request
        api_logger.log_request(
            request_id=request_id,
            endpoint="/chat/validate",
            method="POST",
            payload={}
        )

        # In a real implementation, this might check database connections,
        # external API availability, etc.
        response_data = {
            "status": "available",
            "message": "RAG backend is ready to process queries",
            "timestamp": datetime.utcnow().isoformat()
        }

        # Calculate duration
        duration = (time.time() - start_time) * 1000  # Convert to milliseconds

        # Log the successful response
        api_logger.log_response(
            request_id=request_id,
            status=200,
            payload={"status": "available"},
            duration=duration
        )

        return response_data
    except Exception as e:
        duration = (time.time() - start_time) * 1000  # Convert to milliseconds
        api_logger.log_error(
            request_id=request_id,
            endpoint="/chat/validate",
            error=f"Service validation failed: {str(e)}",
            details={"exception_type": type(e).__name__}
        )
        raise HTTPException(status_code=500, detail=f"Service validation failed: {str(e)}")


# Additional endpoint for testing
@router.get("/chat/test")
async def test_endpoint():
    """
    Test endpoint for development
    """
    return {"message": "Chat API is working", "timestamp": datetime.utcnow().isoformat()}