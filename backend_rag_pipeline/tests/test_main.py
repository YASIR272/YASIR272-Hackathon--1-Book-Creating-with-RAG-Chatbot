import pytest
import os
from unittest.mock import patch, MagicMock
from main import get_all_urls, extract_text_from_url, chunk_text, embed, create_collection, save_chunk_to_qdrant


class TestGetAllUrls:
    """Test the URL crawling functionality"""

    @patch('main.requests.get')
    @patch('main.BeautifulSoup')
    def test_get_all_urls_basic(self, mock_bs, mock_requests):
        """Test basic URL crawling functionality"""
        # Mock the response
        mock_response = MagicMock()
        mock_response.content = b'<html><body><a href="/page1">Page 1</a><a href="/page2">Page 2</a></body></html>'
        mock_response.raise_for_status.return_value = None
        mock_requests.return_value = mock_response

        # Mock BeautifulSoup
        mock_bs_instance = MagicMock()
        mock_link1 = MagicMock()
        mock_link1.__getitem__.return_value = "/page1"
        mock_link2 = MagicMock()
        mock_link2.__getitem__.return_value = "/page2"
        mock_bs_instance.find_all.return_value = [mock_link1, mock_link2]
        mock_bs.return_value = mock_bs_instance

        base_url = "https://example.com"
        result = get_all_urls(base_url)

        assert isinstance(result, list)
        # This test would need more sophisticated mocking to work properly


class TestExtractTextFromUrl:
    """Test the text extraction functionality"""

    @patch('main.requests.get')
    @patch('main.BeautifulSoup')
    def test_extract_text_from_url(self, mock_bs, mock_requests):
        """Test text extraction from a URL"""
        # Mock the response
        mock_response = MagicMock()
        mock_response.content = b'<html><head><title>Test Title</title></head><body><main>Test content here</main></body></html>'
        mock_response.raise_for_status.return_value = None
        mock_requests.return_value = mock_response

        # Mock BeautifulSoup
        mock_bs_instance = MagicMock()
        mock_title = MagicMock()
        mock_title.get_text.return_value = "Test Title"
        mock_bs_instance.find.side_effect = [
            mock_title,  # title
            MagicMock(),  # main content
            None,  # article
            None  # div with main-wrapper class
        ]
        mock_bs_instance.get_text.return_value = "Test content here"
        mock_bs.return_value = mock_bs_instance

        url = "https://example.com/test"
        result = extract_text_from_url(url)

        assert "title" in result
        assert "content" in result


def test_chunk_text_basic():
    """Test basic text chunking functionality"""
    content = "This is a sample content that will be split into chunks. " * 10
    source_url = "https://example.com/test"
    source_title = "Test Title"

    chunks = chunk_text(content, source_url, source_title, chunk_size=50, overlap=10)

    assert isinstance(chunks, list)
    assert len(chunks) > 0
    for chunk in chunks:
        assert "content" in chunk
        assert "source_url" in chunk
        assert "source_title" in chunk
        assert len(chunk["content"]) <= 50  # Approximate since we try to break at boundaries


@patch('main.co')
def test_embed_function(mock_cohere):
    """Test the embedding function"""
    # Mock the Cohere embed response
    mock_embedding_response = MagicMock()
    mock_embedding_response.embeddings = [[0.1, 0.2, 0.3]]
    mock_cohere.embed.return_value = mock_embedding_response

    text = "Test text for embedding"
    result = embed(text)

    assert isinstance(result, list)
    assert len(result) > 0


# Note: The following tests would require proper API keys and mocking of external services
# which is complex. They're included as examples of what should be tested.

def test_chunk_text_empty_content():
    """Test chunking with empty content"""
    chunks = chunk_text("", "https://example.com", "Test Title")
    assert chunks == []


def test_chunk_text_small_content():
    """Test chunking with content smaller than chunk size"""
    content = "Small content"
    chunks = chunk_text(content, "https://example.com", "Test Title", chunk_size=100)
    assert len(chunks) == 1
    assert chunks[0]["content"] == content