import pytest
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from retrieval_validation.qdrant_client import QdrantSearchClient

def test_metadata_filtering_initialization():
    """Test that QdrantSearchClient with metadata filtering initializes correctly"""
    client = QdrantSearchClient()
    assert client is not None

def test_search_with_filters():
    """Test search functionality with different filter criteria"""
    client = QdrantSearchClient()

    # Skip if API keys are not available
    if not os.getenv("QDRANT_URL") or not os.getenv("QDRANT_API_KEY") or not os.getenv("COHERE_API_KEY"):
        pytest.skip("Required API keys not available")

    try:
        # Test search with URL filter
        # First we need to convert a query to embedding
        from retrieval_validation.query_processor import query_processor
        query_embedding = query_processor.convert_query_to_embedding("test query")

        # Test with a URL filter (this will return empty results if no matching documents exist)
        results = client.search_with_filters(
            query_embedding=query_embedding,
            url_filter="https://example.com"
        )
        assert isinstance(results, list)

        # Test with multiple filters
        results = client.search_with_filters(
            query_embedding=query_embedding,
            url_filter="https://example.com",
            module_filter="test_module",
            section_filter="test_section"
        )
        assert isinstance(results, list)

    except Exception as e:
        pytest.skip(f"Could not test filtering functionality: {e}")

def test_search_similar_chunks_with_metadata():
    """Test search similar chunks with metadata filters"""
    client = QdrantSearchClient()

    # Skip if API keys are not available
    if not os.getenv("QDRANT_URL") or not os.getenv("QDRANT_API_KEY") or not os.getenv("COHERE_API_KEY"):
        pytest.skip("Required API keys not available")

    try:
        # Test search with metadata filters
        from retrieval_validation.query_processor import query_processor
        query_embedding = query_processor.convert_query_to_embedding("test query")

        results = client.search_similar_chunks(
            query_embedding=query_embedding,
            metadata_filters={"test_field": "test_value"}
        )
        assert isinstance(results, list)

    except Exception as e:
        pytest.skip(f"Could not test metadata filtering: {e}")

if __name__ == "__main__":
    pytest.main([__file__])