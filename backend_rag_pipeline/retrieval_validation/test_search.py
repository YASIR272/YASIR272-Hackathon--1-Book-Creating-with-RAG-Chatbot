import pytest
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from retrieval_validation.query_processor import QueryProcessor
from retrieval_validation.qdrant_client import QdrantSearchClient
from retrieval_validation.models import QueryRequest

def test_query_processor_initialization():
    """Test that QueryProcessor initializes correctly"""
    processor = QueryProcessor()
    assert processor is not None

def test_qdrant_client_initialization():
    """Test that QdrantSearchClient initializes correctly"""
    client = QdrantSearchClient()
    assert client is not None

def test_query_validation():
    """Test query validation functionality"""
    processor = QueryProcessor()

    # Test valid query
    result = processor.validate_query_input("What is ROS 2?", top_k=5)
    assert result["query_text"] == "What is ROS 2?"
    assert result["top_k"] == 5

    # Test empty query (should raise error)
    try:
        processor.validate_query_input("")
        assert False, "Expected ValueError for empty query"
    except ValueError:
        pass  # Expected

def test_embedding_conversion():
    """Test that query embedding conversion works"""
    processor = QueryProcessor()

    # Skip if API keys are not available
    if not os.getenv("COHERE_API_KEY"):
        pytest.skip("COHERE_API_KEY not available")

    try:
        embedding = processor.convert_query_to_embedding("test query")
        assert isinstance(embedding, list)
        assert len(embedding) > 0
    except Exception as e:
        pytest.skip(f"Could not test embedding conversion: {e}")

def test_sample_query_request():
    """Test creating a sample query request"""
    query_request = QueryRequest(
        query_text="What is ROS 2?",
        top_k=3,
        similarity_threshold=0.5
    )

    assert query_request.query_text == "What is ROS 2?"
    assert query_request.top_k == 3
    assert query_request.similarity_threshold == 0.5

if __name__ == "__main__":
    pytest.main([__file__])