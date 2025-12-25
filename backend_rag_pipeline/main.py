import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import cohere
from qdrant_client import QdrantClient
from qdrant_client.http import models
from dotenv import load_dotenv
import time
import logging
from typing import List, Dict, Any

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Cohere client
cohere_api_key = os.getenv("COHERE_API_KEY")
if not cohere_api_key:
    raise ValueError("COHERE_API_KEY environment variable is required")
co = cohere.Client(cohere_api_key)

# Initialize Qdrant client
qdrant_url = os.getenv("QDRANT_URL")
qdrant_api_key = os.getenv("QDRANT_API_KEY")
if not qdrant_url or not qdrant_api_key:
    raise ValueError("QDRANT_URL and QDRANT_API_KEY environment variables are required")
qdrant_client = QdrantClient(url=qdrant_url, api_key=qdrant_api_key, timeout=10)


def get_all_urls(base_url: str) -> List[str]:
    """
    Crawl the Docusaurus site and return all valid page URLs
    """
    urls = set()
    visited = set()

    # Start with the base URL
    to_visit = [base_url]

    while to_visit:
        current_url = to_visit.pop(0)

        if current_url in visited or not current_url.startswith(base_url):
            continue

        visited.add(current_url)
        logger.info(f"Crawling: {current_url}")

        try:
            response = requests.get(current_url, timeout=10)
            response.raise_for_status()

            # Add current URL to our list
            urls.add(current_url)

            # Parse the HTML to find more links
            soup = BeautifulSoup(response.content, 'html.parser')

            # Find all links in the page
            for link in soup.find_all('a', href=True):
                href = link['href']
                full_url = urljoin(current_url, href)

                # Only add URLs that are part of the same domain and haven't been visited
                if full_url.startswith(base_url) and full_url not in visited:
                    to_visit.append(full_url)

            # Respectful delay to avoid overwhelming the server
            time.sleep(0.5)

        except requests.RequestException as e:
            logger.error(f"Error crawling {current_url}: {e}")
            continue

    return list(urls)


def extract_text_from_url(url: str) -> Dict[str, str]:
    """
    Extract clean text content from a given URL
    """
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')

        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()

        # Try to find the main content area (Docusaurus specific selectors)
        main_content = soup.find('main') or soup.find('article') or soup.find('div', class_='main-wrapper') or soup

        # Extract text content
        text_content = main_content.get_text(separator=' ', strip=True)

        # Extract title
        title = soup.find('title')
        title_text = title.get_text().strip() if title else "No Title"

        # Clean up the text
        lines = (line.strip() for line in text_content.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text_content = ' '.join(chunk for chunk in chunks if chunk)

        return {
            'title': title_text,
            'content': text_content
        }
    except Exception as e:
        logger.error(f"Error extracting text from {url}: {e}")
        return {
            'title': "Error",
            'content': ""
        }


def chunk_text(content: str, source_url: str, source_title: str, chunk_size: int = 1000, overlap: int = 100) -> List[Dict[str, Any]]:
    """
    Split content into appropriately sized chunks with metadata
    """
    if not content:
        return []

    chunks = []
    start = 0

    while start < len(content):
        end = start + chunk_size

        # If we're near the end, just take the remaining content
        if end > len(content):
            end = len(content)
        else:
            # Try to break at a sentence or word boundary
            while end > start + chunk_size - overlap and end < len(content) and content[end] not in '.!? ':
                end += 1

            if end == start + chunk_size - overlap:
                # If we couldn't find a good break point, just take the chunk
                end = start + chunk_size

        chunk_text = content[start:end].strip()

        if chunk_text:  # Only add non-empty chunks
            chunk = {
                'id': f"{source_url}#{start}",
                'content': chunk_text,
                'source_url': source_url,
                'source_title': source_title,
                'section_info': {
                    'start_pos': start,
                    'end_pos': end
                },
                'metadata': {
                    'created_at': time.time()
                }
            }
            chunks.append(chunk)

        # Move start position with overlap
        start = end - overlap if end < len(content) else end

    return chunks


def embed(text: str) -> List[float]:
    """
    Generate embedding vector for text using Cohere API
    """
    try:
        response = co.embed(
            texts=[text],
            model="embed-english-v3.0",
            input_type="search_document"
        )
        return response.embeddings[0]
    except Exception as e:
        logger.error(f"Error generating embedding for text: {e}")
        raise


def create_collection(collection_name: str):
    """
    Create a Qdrant collection for storing embeddings
    """
    try:
        # Check if collection already exists
        try:
            qdrant_client.get_collection(collection_name)
            logger.info(f"Collection '{collection_name}' already exists")
            return
        except:
            pass  # Collection doesn't exist, so we'll create it

        # Get embedding size from Cohere (for embed-english-v3.0, it's 1024)
        sample_embedding = embed("This is a sample text for testing")
        embedding_size = len(sample_embedding)

        # Create the collection
        qdrant_client.create_collection(
            collection_name=collection_name,
            vectors_config=models.VectorParams(
                size=embedding_size,
                distance=models.Distance.COSINE
            )
        )
        logger.info(f"Created collection '{collection_name}' with vector size {embedding_size}")
    except Exception as e:
        logger.error(f"Error creating collection '{collection_name}': {e}")
        raise


def save_chunk_to_qdrant(chunk: Dict[str, Any], embedding: List[float], collection_name: str = "book_embedding"):
    """
    Save a text chunk with its embedding to Qdrant
    """
    try:
        qdrant_client.upsert(
            collection_name=collection_name,
            points=[
                models.PointStruct(
                    id=chunk['id'].replace('/', '_').replace('#', '_'),  # Qdrant ID must be string/integer
                    vector=embedding,
                    payload={
                        "text_content": chunk['content'],
                        "source_url": chunk['source_url'],
                        "source_title": chunk['source_title'],
                        "section_info": chunk['section_info'],
                        "chunk_metadata": chunk['metadata'],
                        "created_at": chunk['metadata']['created_at']
                    }
                )
            ]
        )
        logger.info(f"Saved chunk to Qdrant: {chunk['id']}")
    except Exception as e:
        logger.error(f"Error saving chunk to Qdrant: {e}")
        raise


def search_similar_content(query: str, top_k: int = 5) -> List[Dict[str, Any]]:
    """
    Search for similar content in the Qdrant collection based on a query
    """
    try:
        # Generate embedding for the query
        query_embedding = embed(query)

        # Search in Qdrant
        search_results = qdrant_client.search(
            collection_name="book_embedding",
            query_vector=query_embedding,
            limit=top_k,
            with_payload=True
        )

        # Format results
        results = []
        for result in search_results:
            results.append({
                'content': result.payload.get('text_content', ''),
                'source_url': result.payload.get('source_url', ''),
                'source_title': result.payload.get('source_title', ''),
                'score': result.score,
                'section_info': result.payload.get('section_info', {})
            })

        return results
    except Exception as e:
        logger.error(f"Error searching for similar content: {e}")
        return []


def main():
    """
    Main function to execute the complete RAG pipeline
    """
    logger.info("Starting RAG Pipeline for Book Content")

    # Get the book URL from environment or use default
    book_url = os.getenv("BOOK_URL", "https://frontendbook-theta.vercel.app/")
    logger.info(f"Processing book from URL: {book_url}")

    # Step 1: Get all URLs from the book site
    logger.info("Step 1: Crawling and collecting URLs...")
    urls = get_all_urls(book_url)
    logger.info(f"Found {len(urls)} URLs to process")

    # Step 2: Create the Qdrant collection
    logger.info("Step 2: Creating Qdrant collection...")
    create_collection("book_embedding")

    # Step 3: Process each URL
    logger.info("Step 3: Processing URLs...")
    processed_count = 0

    for i, url in enumerate(urls):
        logger.info(f"Processing URL {i+1}/{len(urls)}: {url}")

        try:
            # Extract content from URL
            content_data = extract_text_from_url(url)

            if not content_data['content']:
                logger.warning(f"No content extracted from {url}, skipping...")
                continue

            # Chunk the content
            chunks = chunk_text(
                content_data['content'],
                url,
                content_data['title']
            )

            # Process each chunk
            for chunk in chunks:
                try:
                    # Generate embedding
                    embedding = embed(chunk['content'])

                    # Save to Qdrant
                    save_chunk_to_qdrant(chunk, embedding, "book_embedding")

                    # Be respectful to APIs
                    time.sleep(0.1)  # Small delay to respect rate limits
                except Exception as e:
                    logger.error(f"Error processing chunk from {url}: {e}")
                    continue

            processed_count += 1

        except Exception as e:
            logger.error(f"Error processing URL {url}: {e}")
            continue

    logger.info(f"Pipeline completed! Processed {processed_count}/{len(urls)} URLs successfully")
    logger.info("Book content has been indexed in Qdrant for RAG applications")

    # Example search to demonstrate functionality
    logger.info("Testing search functionality...")
    sample_query = "What is ROS 2?"
    search_results = search_similar_content(sample_query)
    logger.info(f"Search results for '{sample_query}': {len(search_results)} results found")


if __name__ == "__main__":
    main()