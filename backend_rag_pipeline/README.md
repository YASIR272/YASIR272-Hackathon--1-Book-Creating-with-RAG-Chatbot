# Book Content RAG Pipeline & Agent System

This project implements a complete Retrieval-Augmented Generation (RAG) system that includes:
1. A pipeline that crawls Docusaurus-based book websites, extracts content, generates embeddings, and stores them in a vector database
2. A RAG-enabled agent using OpenAI SDK for intelligent querying of book content
3. Comprehensive retrieval validation system with accuracy testing

## Features

### RAG Pipeline
- Crawls Docusaurus book websites to extract all accessible pages
- Extracts clean text content while preserving structural metadata
- Chunks content with appropriate metadata for embedding
- Generates vector embeddings using Cohere API
- Stores embeddings in Qdrant vector database
- Provides semantic search capabilities for RAG applications

### RAG Agent (NEW)
- **NEW**: OpenAI-powered agent for natural language queries on book content
- **NEW**: Supports both full-book and selected-text query modes
- **NEW**: Provides structured responses with source citations and confidence scores
- **NEW**: FastAPI endpoints for agent queries
- **NEW**: Confidence scoring based on similarity scores and chunk count
- **NEW**: Source reference generation with URLs and metadata

### Retrieval Validation (NEW)
- **NEW**: Comprehensive retrieval validation system with accuracy testing
- **NEW**: Metadata filtering by URL, module, section, and custom fields
- **NEW**: Validation API endpoints for single queries and test suites
- **NEW**: Configurable similarity thresholds and result limits
- **NEW**: Detailed logging and performance monitoring

## Prerequisites

- Python 3.11+
- OpenAI API key (for agent functionality)
- Cohere API key (for embedding generation)
- Qdrant Cloud account and API key

## Setup

1. Clone the repository
2. Navigate to the `backend_rag_pipeline` directory
3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Copy the `.env.example` file to `.env` and fill in your API keys:

```bash
cp .env.example .env
```

5. Update the environment variables in `.env`:
   - `OPENAI_API_KEY`: Your OpenAI API key (for agent functionality)
   - `COHERE_API_KEY`: Your Cohere API key (for embedding generation)
   - `QDRANT_URL`: Your Qdrant Cloud URL
   - `QDRANT_API_KEY`: Your Qdrant API key
   - `BOOK_URL`: The URL of the Docusaurus book to crawl (default: https://frontendbook-theta.vercel.app/)

## Usage

### RAG Pipeline

To run the complete RAG pipeline (crawling, extraction, embedding, and storage):

```bash
python main.py
```

This will:
1. Crawl the specified book website
2. Extract content from all pages
3. Chunk the content appropriately
4. Generate embeddings for each chunk
5. Store the embeddings in Qdrant with metadata

### RAG Agent API

To run the RAG Agent API server:

```bash
uvicorn api.main:app --reload --port 8000
```

The API provides the following endpoints:
- `GET /` - Root endpoint
- `GET /health` - Health check endpoint
- `POST /agent/query` - Query the RAG agent with natural language queries
- `GET /docs` - API documentation

Example API call:
```bash
curl -X POST "http://localhost:8000/agent/query" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What does the book say about RAG systems?",
    "scope": "full_book",
    "max_results": 5,
    "min_similarity": 0.5
  }'
```

## Architecture

The system consists of three main components:

### 1. RAG Pipeline (main.py)
- `get_all_urls()`: Crawls the book website and collects all page URLs
- `extract_text_from_url()`: Extracts clean text content from a URL
- `chunk_text()`: Splits content into appropriately sized chunks with metadata
- `embed()`: Generates embeddings using Cohere API
- `create_collection()`: Creates a Qdrant collection for storing embeddings
- `save_chunk_to_qdrant()`: Saves chunks with embeddings to Qdrant
- `search_similar_content()`: Searches for similar content in Qdrant
- `main()`: Orchestrates the complete pipeline

### 2. RAG Agent System (agents/ directory)
- `rag_agent.py`: Main RAG agent implementation with query processing and confidence scoring
- `retrieval_tools.py`: Tools for retrieving content from Qdrant for the agent
- `agents_router.py`: FastAPI router for agent endpoints
- `api/models.py`: API request/response models for agent interactions
- `models/agent_models.py`: Internal data models for agent operations
- `services/retrieval_service.py`: Service layer for content retrieval operations

### 3. RAG Retrieval Validation System (retrieval_validation/ directory)
- `models.py`: Pydantic models for API requests/responses
- `query_processor.py`: Query processing and embedding conversion
- `qdrant_client.py`: Qdrant search operations with metadata filtering
- `validation_engine.py`: Accuracy validation and test suite execution
- `api.py`: FastAPI application with search and validation endpoints

## Testing

Run the tests with pytest:

```bash
pytest tests/
```

## Configuration

The pipeline can be configured through environment variables in the `.env` file:

- `BOOK_URL`: The base URL of the Docusaurus book to crawl
- `CHUNK_SIZE`: Size of text chunks (default: 1000 characters)
- `CHUNK_OVERLAP`: Overlap between chunks (default: 100 characters)

## Performance

### RAG Pipeline
- Process 100 pages per hour with 95% success rate
- Maintain sub-2s query response time for semantic searches
- Handle books up to 1000 pages and 1 million words of content

### RAG Agent
- Sub-3s response time for agent queries with source citations
- Support for concurrent agent queries with proper resource management
- Confidence scoring with 0.0-1.0 range based on similarity and chunk count