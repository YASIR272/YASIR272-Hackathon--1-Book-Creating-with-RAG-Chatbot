import pytest
import asyncio
from unittest.mock import AsyncMock, MagicMock, patch
from agents.rag_agent import RAGAgent
from api.models import AgentQueryRequest
from models.agent_models import RetrievedChunk


class TestRAGAgent:
    """Unit tests for the RAG Agent"""

    def setup_method(self):
        """Set up test fixtures before each test method."""
        self.agent = RAGAgent()
        self.sample_request = AgentQueryRequest(
            query="Test query about book content",
            scope="full_book",
            max_results=5,
            min_similarity=0.5
        )
        self.sample_chunks = [
            RetrievedChunk(
                id="chunk_1",
                content="This is sample content from the book.",
                similarity_score=0.85,
                source_url="https://example.com/page1",
                source_title="Sample Page 1",
                metadata={"section": "1.1", "module": "intro"}
            ),
            RetrievedChunk(
                id="chunk_2",
                content="This is more sample content from the book.",
                similarity_score=0.75,
                source_url="https://example.com/page2",
                source_title="Sample Page 2",
                metadata={"section": "1.2", "module": "intro"}
            )
        ]

    @pytest.mark.asyncio
    async def test_query_method_success(self):
        """Test that the query method returns a valid response"""
        with patch.object(self.agent, '_retrieve_context', return_value=self.sample_chunks) as mock_retrieve, \
             patch.object(self.agent, '_generate_response_with_context', return_value="Generated response") as mock_generate:

            response = await self.agent.query(self.sample_request)

            # Assertions
            assert response.response == "Generated response"
            assert response.retrieved_chunks_count == 2
            assert response.confidence > 0.0
            assert response.query_time >= 0

            # Verify the helper methods were called
            mock_retrieve.assert_called_once()
            mock_generate.assert_called_once()

    @pytest.mark.asyncio
    async def test_query_method_with_empty_chunks(self):
        """Test that the query method handles empty chunks gracefully"""
        with patch.object(self.agent, '_retrieve_context', return_value=[]) as mock_retrieve, \
             patch.object(self.agent, '_generate_response_with_context', return_value="No relevant information found") as mock_generate:

            response = await self.agent.query(self.sample_request)

            # Assertions
            assert response.response == "No relevant information found"
            assert response.retrieved_chunks_count == 0
            assert response.confidence == 0.0
            assert response.query_time >= 0

    @pytest.mark.asyncio
    async def test_query_method_exception_handling(self):
        """Test that the query method handles exceptions gracefully"""
        with patch.object(self.agent, '_retrieve_context', side_effect=Exception("Test error")):

            response = await self.agent.query(self.sample_request)

            # Assertions
            assert "An error occurred while processing your query" in response.response
            assert response.retrieved_chunks_count == 0
            assert response.confidence == 0.0
            assert response.query_time >= 0

    def test_calculate_confidence_score_with_chunks(self):
        """Test confidence calculation with retrieved chunks"""
        chunks = [
            RetrievedChunk(
                id="chunk_1",
                content="Test content",
                similarity_score=0.9,
                source_url="https://example.com",
                source_title="Test Page",
                metadata={}
            ),
            RetrievedChunk(
                id="chunk_2",
                content="Test content",
                similarity_score=0.7,
                source_url="https://example.com",
                source_title="Test Page",
                metadata={}
            )
        ]

        confidence = self.agent.calculate_confidence_score(chunks)

        # Should be between 0 and 1
        assert 0.0 <= confidence <= 1.0

        # With 2 chunks and avg similarity of 0.8, confidence should be reasonable
        assert confidence > 0.5

    def test_calculate_confidence_score_empty_chunks(self):
        """Test confidence calculation with no chunks"""
        confidence = self.agent.calculate_confidence_score([])

        assert confidence == 0.0

    @pytest.mark.asyncio
    async def test_retrieve_context_method(self):
        """Test the _retrieve_context method"""
        with patch('agents.rag_agent.settings') as mock_settings, \
             patch('agents.rag_agent.openai') as mock_openai:

            # Mock the OpenAI API response
            mock_embedding_response = MagicMock()
            mock_embedding_response.data = [MagicMock()]
            mock_embedding_response.data[0].embedding = [0.1, 0.2, 0.3]

            mock_openai.embeddings.create = AsyncMock(return_value=mock_embedding_response)

            # Mock the retrieval service
            with patch('agents.rag_agent.retrieval_service') as mock_retrieval_service:
                mock_retrieval_service.retrieve_context_with_scope.return_value = self.sample_chunks

                chunks = await self.agent._retrieve_context(
                    query_text="test query",
                    scope="full_book",
                    scope_filters=None,
                    top_k=5
                )

                # Assertions
                assert len(chunks) == 2
                assert chunks == self.sample_chunks
                mock_retrieval_service.retrieve_context_with_scope.assert_called_once()

    @pytest.mark.asyncio
    async def test_generate_response_with_context_with_chunks(self):
        """Test response generation with context"""
        response = await self.agent._generate_response_with_context(
            query_text="What does the book say?",
            retrieved_chunks=self.sample_chunks
        )

        # Should contain the query and sources
        assert "What does the book say?" in response
        assert "Sources used" in response
        assert "Sample Page 1" in response or "Sample Page 2" in response

    @pytest.mark.asyncio
    async def test_generate_response_with_context_no_chunks(self):
        """Test response generation with no context"""
        response = await self.agent._generate_response_with_context(
            query_text="What does the book say?",
            retrieved_chunks=[]
        )

        # Should return a message indicating no relevant information
        assert "couldn't find any relevant information" in response