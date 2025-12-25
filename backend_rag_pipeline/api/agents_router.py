from fastapi import APIRouter, HTTPException, Request
from typing import Dict, Any
import time
from config.logging import logger
from api.models import AgentQueryRequest, AgentQueryResponse
from agents.rag_agent import rag_agent
from slowapi import Limiter
from slowapi.util import get_remote_address


# Create router for agent-related endpoints
agents_router = APIRouter(prefix="/agent", tags=["agent"])

# Create rate limiter for this router
limiter = Limiter(key_func=get_remote_address)


@agents_router.post("/query", response_model=AgentQueryResponse)
@limiter.limit("10/minute")  # Limit to 10 requests per minute per IP
async def query_agent(request: AgentQueryRequest) -> AgentQueryResponse:
    """
    Query the RAG agent with natural language questions about book content
    """
    start_time = time.time()
    logger.info(f"Agent query received: '{request.query[:50]}...'")

    try:
        # Validate request parameters
        if not request.query or len(request.query.strip()) == 0:
            raise HTTPException(status_code=422, detail="Query cannot be empty")

        if len(request.query) > 1000:
            raise HTTPException(status_code=422, detail="Query too long, maximum 1000 characters")

        # Process the query with the RAG agent
        response = await rag_agent.query(request)

        query_time = time.time() - start_time
        logger.info(f"Agent query processed in {query_time:.2f}s")

        return response

    except HTTPException:
        # Re-raise HTTP exceptions as they are
        raise
    except Exception as e:
        query_time = time.time() - start_time
        logger.error(f"Error processing agent query after {query_time:.2f}s: {e}")
        raise HTTPException(status_code=500, detail=f"Error processing query: {str(e)}")


@agents_router.get("/health")
@limiter.limit("30/minute")  # Limit to 30 health check requests per minute per IP
async def agent_health() -> Dict[str, Any]:
    """
    Health check for the agent service
    """
    try:
        # Perform a basic check (e.g., check if services are accessible)
        return {
            "status": "healthy",
            "timestamp": time.time(),
            "service": "rag-agent"
        }
    except Exception as e:
        logger.error(f"Agent health check failed: {e}")
        raise HTTPException(status_code=503, detail="Agent service unhealthy")