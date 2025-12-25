# Quickstart Guide for RAG Agent API

This guide will help you quickly set up and test the RAG Agent API.

## Prerequisites

- Python 3.11+
- OpenAI API key
- Qdrant Cloud account and API key
- Cohere API key (for embedding generation)

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Create environment file:
```bash
cp .env.example .env
```

3. Update environment variables in `.env`:
```
OPENAI_API_KEY=your_openai_api_key_here
COHERE_API_KEY=your_cohere_api_key_here
QDRANT_URL=your_qdrant_url_here
QDRANT_API_KEY=your_qdrant_api_key_here
BOOK_URL=https://frontendbook-theta.vercel.app/
```

## Running the System

### 1. Run the RAG Pipeline (to populate the vector database)

```bash
python main.py
```

This will crawl the book website, extract content, generate embeddings, and store them in Qdrant.

### 2. Start the RAG Agent API

```bash
uvicorn api.main:app --reload --port 8000
```

### 3. Test the API

Once the API is running, you can test it with curl:

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

Or using Python:

```python
import requests

response = requests.post("http://localhost:8000/agent/query", json={
    "query": "What does the book say about RAG systems?",
    "scope": "full_book",
    "max_results": 5,
    "min_similarity": 0.5
})

print(response.json())
```

## API Endpoints

- `GET /` - Root endpoint
- `GET /health` - Health check
- `GET /docs` - API documentation
- `POST /agent/query` - Query the RAG agent
- `GET /agent/health` - Agent-specific health check

## Configuration

You can configure rate limiting and allowed origins via environment variables:

```
ALLOWED_ORIGINS=http://localhost,http://127.0.0.1
ALLOWED_HOSTS=localhost,127.0.0.1
ROOT_PATH=
```

Rate limits:
- Agent query: 10 requests/minute per IP
- Health checks: 30 requests/minute per IP
- Root endpoint: 100 requests/minute per IP
- Docs endpoint: 50 requests/minute per IP