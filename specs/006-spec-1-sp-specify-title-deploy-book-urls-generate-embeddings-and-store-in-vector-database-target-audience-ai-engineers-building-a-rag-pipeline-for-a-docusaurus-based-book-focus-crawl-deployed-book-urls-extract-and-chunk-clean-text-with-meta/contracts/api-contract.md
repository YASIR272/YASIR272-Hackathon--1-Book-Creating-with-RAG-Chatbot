# API Contract: RAG Pipeline Service

## Overview
This document defines the contract for the RAG pipeline service that processes Docusaurus book content and stores it in Qdrant for retrieval.

## Data Models

### TextChunk
```json
{
  "id": "string",
  "content": "string",
  "source_url": "string",
  "source_title": "string",
  "section_info": {},
  "metadata": {}
}
```

### EmbeddingRequest
```json
{
  "text": "string",
  "model": "string"
}
```

### EmbeddingResponse
```json
{
  "id": "string",
  "vector": "array[float]",
  "text_content": "string"
}
```

## Endpoints

Since this implementation is primarily a data processing pipeline that runs as a script, the main "contract" is the function interface defined in main.py:

### Core Functions

#### `get_all_urls(base_url: str) -> List[str]`
- **Purpose**: Crawl the Docusaurus site and return all valid page URLs
- **Input**: Base URL of the book site
- **Output**: List of all discovered page URLs

#### `extract_text_from_url(url: str) -> Dict`
- **Purpose**: Extract clean text content from a given URL
- **Input**: URL to extract content from
- **Output**: Dictionary with 'title' and 'content' keys

#### `chunk_text(content: str, source_url: str, source_title: str) -> List[TextChunk]`
- **Purpose**: Split content into appropriately sized chunks with metadata
- **Input**: Content string, source URL and title
- **Output**: List of TextChunk objects

#### `embed(text: str) -> List[float]`
- **Purpose**: Generate embedding vector for text using Cohere API
- **Input**: Text to embed
- **Output**: Embedding vector as list of floats

#### `create_collection(collection_name: str)`
- **Purpose**: Create a Qdrant collection for storing embeddings
- **Input**: Name of the collection to create
- **Output**: None

#### `save_chunk_to_qdrant(chunk: TextChunk, embedding: List[float])`
- **Purpose**: Save a text chunk with its embedding to Qdrant
- **Input**: TextChunk object and its embedding vector
- **Output**: None

## Error Handling

All functions should raise appropriate exceptions with descriptive messages:
- NetworkError for connection issues
- APIError for service API failures
- ProcessingError for content processing failures