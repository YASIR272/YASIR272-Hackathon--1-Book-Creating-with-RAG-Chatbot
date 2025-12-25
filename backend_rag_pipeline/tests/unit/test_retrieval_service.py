import pytest
from unittest.mock import MagicMock, patch
from services.retrieval_service import RetrievalService
from models.agent_models import RetrievedChunk


class TestRetrievalService:
    """Unit tests for the Retrieval Service"""

    def setup_method(self):
        """Set up test fixtures before each test method."""
        self.service = RetrievalService()
        self.sample_embedding = [0.1, 0.2, 0.3, 0.4, 0.5] * 307  # 1536-dim vector
        self.sample_result = {
            'id': 'test_id',
            'content': 'Test content from the book',
            'score': 0.85,
            'source_url': 'https://example.com/page',
            'source_title': 'Test Page',
            'metadata': {'section': '1.1', 'module': 'intro'}
        }

    def test_retrieve_context_success(self):
        """Test successful context retrieval"""
        with patch('services.retrieval_service.qdrant_service') as mock_qdrant:
            mock_qdrant.search_similar.return_value = [self.sample_result]

            chunks = self.service.retrieve_context(
                query_embedding=self.sample_embedding,
                collection_name="test_collection",
                top_k=5
            )

            # Assertions
            assert len(chunks) == 1
            assert isinstance(chunks[0], RetrievedChunk)
            assert chunks[0].id == 'test_id'
            assert chunks[0].content == 'Test content from the book'
            assert chunks[0].similarity_score == 0.85
            assert chunks[0].source_url == 'https://example.com/page'
            assert chunks[0].source_title == 'Test Page'
            assert chunks[0].metadata == {'section': '1.1', 'module': 'intro'}

            mock_qdrant.search_similar.assert_called_once_with(
                collection_name="test_collection",
                query_vector=self.sample_embedding,
                top_k=5,
                filters=None
            )

    def test_retrieve_context_with_filters(self):
        """Test context retrieval with filters"""
        filters = {"section": "1.1"}
        with patch('services.retrieval_service.qdrant_service') as mock_qdrant:
            mock_qdrant.search_similar.return_value = [self.sample_result]

            chunks = self.service.retrieve_context(
                query_embedding=self.sample_embedding,
                collection_name="test_collection",
                top_k=5,
                filters=filters
            )

            # Assertions
            assert len(chunks) == 1
            mock_qdrant.search_similar.assert_called_once_with(
                collection_name="test_collection",
                query_vector=self.sample_embedding,
                top_k=5,
                filters=filters
            )

    def test_retrieve_context_exception_handling(self):
        """Test context retrieval exception handling"""
        with patch('services.retrieval_service.qdrant_service') as mock_qdrant:
            mock_qdrant.search_similar.side_effect = Exception("Test error")

            with pytest.raises(Exception):
                self.service.retrieve_context(
                    query_embedding=self.sample_embedding,
                    collection_name="test_collection",
                    top_k=5
                )

    def test_retrieve_context_with_scope_full_book(self):
        """Test scoped context retrieval with full book scope"""
        with patch('services.retrieval_service.qdrant_service') as mock_qdrant:
            mock_qdrant.search_similar.return_value = [self.sample_result]

            chunks = self.service.retrieve_context_with_scope(
                query_embedding=self.sample_embedding,
                scope="full_book",
                top_k=5
            )

            # Assertions
            assert len(chunks) == 1
            mock_qdrant.search_similar.assert_called_once_with(
                collection_name="book_embedding",
                query_vector=self.sample_embedding,
                top_k=5,
                filters=None  # No filters for full book
            )

    def test_retrieve_context_with_scope_selected_text(self):
        """Test scoped context retrieval with selected text scope"""
        scope_filters = {"section": "1.1", "module": "intro"}
        with patch('services.retrieval_service.qdrant_service') as mock_qdrant:
            mock_qdrant.search_similar.return_value = [self.sample_result]

            chunks = self.service.retrieve_context_with_scope(
                query_embedding=self.sample_embedding,
                scope="selected_text",
                scope_filters=scope_filters,
                top_k=5
            )

            # Assertions
            assert len(chunks) == 1
            mock_qdrant.search_similar.assert_called_once_with(
                collection_name="book_embedding",
                query_vector=self.sample_embedding,
                top_k=5,
                filters=scope_filters  # Filters applied for selected text
            )

    def test_retrieve_context_with_scope_unknown_scope(self):
        """Test scoped context retrieval with unknown scope"""
        with patch('services.retrieval_service.qdrant_service') as mock_qdrant:
            mock_qdrant.search_similar.return_value = [self.sample_result]

            chunks = self.service.retrieve_context_with_scope(
                query_embedding=self.sample_embedding,
                scope="unknown_scope",
                top_k=5
            )

            # Assertions
            assert len(chunks) == 1
            # Should default to full book (no filters)
            mock_qdrant.search_similar.assert_called_once_with(
                collection_name="book_embedding",
                query_vector=self.sample_embedding,
                top_k=5,
                filters=None
            )

    def test_get_collection_info(self):
        """Test getting collection information"""
        expected_info = {"vectors_count": 100, "indexed_vectors_count": 100}
        with patch('services.retrieval_service.qdrant_service') as mock_qdrant:
            mock_qdrant.get_collection_info.return_value = expected_info

            info = self.service.get_collection_info("test_collection")

            # Assertions
            assert info == expected_info
            mock_qdrant.get_collection_info.assert_called_once_with("test_collection")

    def test_get_collection_info_exception_handling(self):
        """Test getting collection information exception handling"""
        with patch('services.retrieval_service.qdrant_service') as mock_qdrant:
            mock_qdrant.get_collection_info.side_effect = Exception("Test error")

            with pytest.raises(Exception):
                self.service.get_collection_info("test_collection")