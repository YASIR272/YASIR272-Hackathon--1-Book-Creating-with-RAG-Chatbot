import pytest
from pydantic import ValidationError
from api.models import AgentQueryRequest, AgentQueryResponse, HealthCheckResponse, SourceReference
from models.agent_models import RetrievedChunk


class TestAgentQueryRequest:
    """Unit tests for AgentQueryRequest model"""

    def test_agent_query_request_valid(self):
        """Test creating a valid AgentQueryRequest"""
        request = AgentQueryRequest(
            query="What does the book say about RAG systems?",
            scope="full_book",
            max_results=5,
            min_similarity=0.5
        )

        # Assertions
        assert request.query == "What does the book say about RAG systems?"
        assert request.scope == "full_book"
        assert request.max_results == 5
        assert request.min_similarity == 0.5

    def test_agent_query_request_default_values(self):
        """Test default values for AgentQueryRequest"""
        request = AgentQueryRequest(
            query="Test query"
        )

        # Assertions
        assert request.scope == "full_book"
        assert request.max_results == 5
        assert request.min_similarity == 0.5

    def test_agent_query_request_query_validation(self):
        """Test query validation"""
        with pytest.raises(ValidationError):
            AgentQueryRequest(
                query=""  # Empty query should fail
            )

        with pytest.raises(ValidationError):
            AgentQueryRequest(
                query="x" * 1001  # Too long query should fail
            )

    def test_agent_query_request_scope_validation(self):
        """Test scope validation"""
        # Valid scopes should work
        request1 = AgentQueryRequest(
            query="Test query",
            scope="full_book"
        )
        assert request1.scope == "full_book"

        request2 = AgentQueryRequest(
            query="Test query",
            scope="selected_text"
        )
        assert request2.scope == "selected_text"

        # Invalid scope should raise ValidationError
        with pytest.raises(ValidationError):
            AgentQueryRequest(
                query="Test query",
                scope="invalid_scope"
            )

    def test_agent_query_request_max_results_validation(self):
        """Test max_results validation"""
        with pytest.raises(ValidationError):
            AgentQueryRequest(
                query="Test query",
                max_results=0  # Should be at least 1
            )

        with pytest.raises(ValidationError):
            AgentQueryRequest(
                query="Test query",
                max_results=101  # Should be at most 100
            )

    def test_agent_query_request_min_similarity_validation(self):
        """Test min_similarity validation"""
        with pytest.raises(ValidationError):
            AgentQueryRequest(
                query="Test query",
                min_similarity=-0.1  # Should be between 0 and 1
            )

        with pytest.raises(ValidationError):
            AgentQueryRequest(
                query="Test query",
                min_similarity=1.1  # Should be between 0 and 1
            )


class TestAgentQueryResponse:
    """Unit tests for AgentQueryResponse model"""

    def test_agent_query_response_valid(self):
        """Test creating a valid AgentQueryResponse"""
        sources = [
            SourceReference(
                content="Test content",
                source_url="https://example.com",
                source_title="Test Page",
                similarity_score=0.8,
                metadata={"section": "1.1"},
                chunk_id="chunk_1"
            )
        ]

        response = AgentQueryResponse(
            response="Generated response",
            sources=sources,
            confidence=0.85,
            query_time=0.5,
            retrieved_chunks_count=1
        )

        # Assertions
        assert response.response == "Generated response"
        assert len(response.sources) == 1
        assert response.confidence == 0.85
        assert response.query_time == 0.5
        assert response.retrieved_chunks_count == 1

    def test_agent_query_response_default_values(self):
        """Test default values for AgentQueryResponse"""
        response = AgentQueryResponse(
            response="Generated response",
            sources=[],
            confidence=0.85,
            query_time=0.5,
            retrieved_chunks_count=1
        )

        # Assertions
        assert response.response == "Generated response"
        assert response.confidence == 0.85
        assert response.query_time == 0.5
        assert response.retrieved_chunks_count == 1


class TestHealthCheckResponse:
    """Unit tests for HealthCheckResponse model"""




class TestSourceReference:
    """Unit tests for SourceReference model"""

    def test_source_reference_valid(self):
        """Test creating a valid SourceReference"""
        source = SourceReference(
            content="Test content from the book",
            source_url="https://example.com/page",
            source_title="Test Page Title",
            similarity_score=0.85,
            metadata={"section": "1.1", "module": "intro"},
            chunk_id="chunk_123"
        )

        # Assertions
        assert source.content == "Test content from the book"
        assert source.source_url == "https://example.com/page"
        assert source.source_title == "Test Page Title"
        assert source.similarity_score == 0.85
        assert source.metadata == {"section": "1.1", "module": "intro"}
        assert source.chunk_id == "chunk_123"

    def test_source_reference_similarity_score_validation(self):
        """Test similarity_score validation"""
        with pytest.raises(ValidationError):
            SourceReference(
                content="Test content",
                source_url="https://example.com",
                source_title="Test Page",
                similarity_score=-0.1,  # Should be between 0 and 1
                metadata={},
                chunk_id="chunk_1"
            )

        with pytest.raises(ValidationError):
            SourceReference(
                content="Test content",
                source_url="https://example.com",
                source_title="Test Page",
                similarity_score=1.1,  # Should be between 0 and 1
                metadata={},
                chunk_id="chunk_1"
            )


class TestRetrievedChunk:
    """Unit tests for RetrievedChunk model (from models.agent_models)"""

    def test_retrieved_chunk_valid(self):
        """Test creating a valid RetrievedChunk"""
        chunk = RetrievedChunk(
            id="chunk_123",
            content="Test content from the book",
            similarity_score=0.85,
            source_url="https://example.com/page",
            source_title="Test Page Title",
            metadata={"section": "1.1", "module": "intro"}
        )

        # Assertions
        assert chunk.id == "chunk_123"
        assert chunk.content == "Test content from the book"
        assert chunk.similarity_score == 0.85
        assert chunk.source_url == "https://example.com/page"
        assert chunk.source_title == "Test Page Title"
        assert chunk.metadata == {"section": "1.1", "module": "intro"}
        assert chunk.vector_embedding is None  # Default value

    def test_retrieved_chunk_with_embedding(self):
        """Test creating a RetrievedChunk with embedding"""
        chunk = RetrievedChunk(
            id="chunk_123",
            content="Test content from the book",
            similarity_score=0.85,
            source_url="https://example.com/page",
            source_title="Test Page Title",
            metadata={"section": "1.1", "module": "intro"},
            vector_embedding=[0.1, 0.2, 0.3]
        )

        # Assertions
        assert chunk.id == "chunk_123"
        assert chunk.vector_embedding == [0.1, 0.2, 0.3]

