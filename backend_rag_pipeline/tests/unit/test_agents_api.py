import pytest
from fastapi.testclient import TestClient
from api.main import app
from unittest.mock import patch, AsyncMock
from models.agent_models import RetrievedChunk


class TestAgentsAPI:
    """Unit tests for the agents API endpoints"""

    def setup_method(self):
        """Set up test fixtures before each test method."""
        self.client = TestClient(app)
        self.sample_chunks = [
            RetrievedChunk(
                id="chunk_1",
                content="This is sample content from the book.",
                similarity_score=0.85,
                source_url="https://example.com/page1",
                source_title="Sample Page 1",
                metadata={"section": "1.1", "module": "intro"}
            )
        ]

    def test_root_endpoint(self):
        """Test the root endpoint"""
        response = self.client.get("/")

        assert response.status_code == 200
        assert response.json() == {"message": "RAG Agent API is running"}

    def test_health_endpoint(self):
        """Test the health check endpoint"""
        response = self.client.get("/health")

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "timestamp" in data

    def test_docs_endpoint(self):
        """Test the docs endpoint"""
        response = self.client.get("/docs")

        assert response.status_code == 200
        assert response.json() == {"message": "API documentation available at /docs"}

    @patch('api.agents_router.rag_agent')
    def test_query_agent_success(self, mock_rag_agent):
        """Test successful agent query"""
        # Mock the agent response
        mock_response = AsyncMock()
        mock_response.response = "Generated response based on book content"
        mock_response.sources = []
        mock_response.confidence = 0.85
        mock_response.query_time = 0.5
        mock_response.retrieved_chunks_count = 1

        # Mock the async query method
        mock_rag_agent.query = AsyncMock(return_value=mock_response)

        # Make the request
        query_data = {
            "query": "What does the book say about RAG systems?",
            "scope": "full_book",
            "max_results": 5,
            "min_similarity": 0.5
        }
        response = self.client.post("/agent/query", json=query_data)

        # Assertions
        assert response.status_code == 200
        data = response.json()
        assert data["response"] == "Generated response based on book content"
        assert data["confidence"] == 0.85
        assert data["query_time"] == 0.5
        assert data["retrieved_chunks_count"] == 1

        # Verify the mock was called
        mock_rag_agent.query.assert_called_once()

    @patch('api.agents_router.rag_agent')
    def test_query_agent_validation_error(self, mock_rag_agent):
        """Test agent query with validation error"""
        # Make the request with invalid data
        query_data = {
            "query": "",  # Empty query should fail validation
            "scope": "full_book"
        }
        response = self.client.post("/agent/query", json=query_data)

        # Assertions
        assert response.status_code == 422  # Validation error

    @patch('api.agents_router.rag_agent')
    def test_query_agent_long_query_error(self, mock_rag_agent):
        """Test agent query with too long query"""
        # Make the request with too long query
        query_data = {
            "query": "x" * 1001,  # Too long query should fail validation
            "scope": "full_book"
        }
        response = self.client.post("/agent/query", json=query_data)

        # Assertions
        assert response.status_code == 422  # Validation error

    @patch('api.agents_router.rag_agent')
    def test_query_agent_exception_handling(self, mock_rag_agent):
        """Test agent query with exception handling"""
        # Mock the agent to raise an exception
        mock_rag_agent.query = AsyncMock(side_effect=Exception("Test error"))

        # Make the request
        query_data = {
            "query": "What does the book say about RAG systems?",
            "scope": "full_book",
            "max_results": 5,
            "min_similarity": 0.5
        }
        response = self.client.post("/agent/query", json=query_data)

        # Assertions
        assert response.status_code == 500  # Internal server error
        data = response.json()
        assert "Error processing query" in data["detail"]

    def test_agent_health_endpoint(self):
        """Test the agent-specific health endpoint"""
        response = self.client.get("/agent/health")

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["service"] == "rag-agent"
        assert "timestamp" in data

    @patch('api.agents_router.rag_agent')
    def test_query_agent_different_scopes(self, mock_rag_agent):
        """Test agent query with different scopes"""
        # Mock the agent response
        mock_response = AsyncMock()
        mock_response.response = "Generated response"
        mock_response.sources = []
        mock_response.confidence = 0.8
        mock_response.query_time = 0.3
        mock_response.retrieved_chunks_count = 1

        mock_rag_agent.query = AsyncMock(return_value=mock_response)

        # Test with selected_text scope
        query_data = {
            "query": "What does the book say?",
            "scope": "selected_text",
            "scope_filters": {"section": "1.1", "module": "intro"},
            "max_results": 5,
            "min_similarity": 0.5
        }
        response = self.client.post("/agent/query", json=query_data)

        # Assertions
        assert response.status_code == 200
        data = response.json()
        assert data["response"] == "Generated response"

    @patch('api.agents_router.rag_agent')
    def test_query_agent_custom_parameters(self, mock_rag_agent):
        """Test agent query with custom parameters"""
        # Mock the agent response
        mock_response = AsyncMock()
        mock_response.response = "Generated response"
        mock_response.sources = []
        mock_response.confidence = 0.9
        mock_response.query_time = 0.4
        mock_response.retrieved_chunks_count = 2

        mock_rag_agent.query = AsyncMock(return_value=mock_response)

        # Test with custom parameters
        query_data = {
            "query": "What does the book say?",
            "scope": "full_book",
            "max_results": 10,  # Custom max results
            "min_similarity": 0.7  # Custom min similarity
        }
        response = self.client.post("/agent/query", json=query_data)

        # Assertions
        assert response.status_code == 200
        data = response.json()
        assert data["response"] == "Generated response"
        assert data["confidence"] == 0.9
        assert data["retrieved_chunks_count"] == 2