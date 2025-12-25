# Quickstart: RAG-Enabled Agent with OpenAI SDK and FastAPI

## Overview
This guide provides quick setup and usage instructions for the RAG-enabled agent system.

## Prerequisites
- Python 3.11+
- OpenAI API key
- Qdrant Cloud account and API key
- Book content already indexed in Qdrant (from previous RAG pipeline)

## Setup

### 1. Install Dependencies
```bash
pip install openai fastapi uvicorn pydantic qdrant-client python-dotenv
```

### 2. Environment Configuration
Create a `.env` file with the following variables:
```bash
OPENAI_API_KEY=your_openai_api_key
QDRANT_URL=your_qdrant_cloud_url
QDRANT_API_KEY=your_qdrant_api_key
```

### 3. Initialize the Agent
```python
from agents.rag_agent import RAGAgent

agent = RAGAgent()
```

## Usage Examples

### 1. Basic Query
```python
from api.models import AgentQueryRequest

request = AgentQueryRequest(
    query="What is the main concept discussed in this book?"
)

response = await agent.query(request)
print(response.response)
```

### 2. Scoped Query (Selected Text Only)
```python
request = AgentQueryRequest(
    query="Explain the implementation details",
    scope="selected_text",
    scope_filters={
        "modules": ["implementation-guide"],
        "sections": ["section-3"]
    }
)

response = await agent.query(request)
print(response.response)
print(f"Sources used: {len(response.sources)}")
```

### 3. FastAPI Endpoint
```bash
# Start the server
uvicorn api.main:app --reload

# Query the agent
curl -X POST "http://localhost:8000/agent/query" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What does the book say about RAG systems?",
    "scope": "full_book",
    "max_results": 3
  }'
```

## API Endpoints

### POST `/agent/query`
Query the RAG agent with natural language.

**Request Body**:
```json
{
  "query": "Natural language query",
  "scope": "full_book",
  "scope_filters": {
    "urls": ["https://example.com/page1"],
    "modules": ["module1"],
    "sections": ["section1"]
  },
  "max_results": 5,
  "min_similarity": 0.7
}
```

**Response**:
```json
{
  "response": "Agent's response to the query",
  "sources": [
    {
      "content": "Retrieved content chunk",
      "source_url": "https://example.com/source",
      "source_title": "Source Title",
      "similarity_score": 0.85,
      "metadata": {},
      "chunk_id": "unique_chunk_id"
    }
  ],
  "confidence": 0.92,
  "query_time": 1.23,
  "retrieved_chunks_count": 3
}
```

## Running Tests
```bash
pytest tests/
```

## Local Development
```bash
# Run the API server
uvicorn api.main:app --reload --port 8000

# Run with auto-reload
uvicorn api.main:app --reload

# Run tests
python -m pytest tests/ -v
```

## Troubleshooting
- Ensure all API keys are properly configured in environment variables
- Verify Qdrant connection and that book content is indexed
- Check that OpenAI API is accessible