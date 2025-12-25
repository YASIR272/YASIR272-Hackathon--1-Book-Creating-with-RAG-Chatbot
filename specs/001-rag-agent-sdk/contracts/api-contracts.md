# API Contracts: RAG-Enabled Agent with OpenAI SDK and FastAPI

## Overview
This document defines the API contracts for the RAG-enabled agent system, including request/response schemas, endpoints, and integration patterns.

## Base URL
`http://localhost:8000` (or configured host/port)

## Authentication
None required for initial implementation (to be added in future iterations)

## Endpoints

### POST /agent/query
Query the RAG agent with natural language questions about book content.

**Description**: Submit a natural language query to the RAG agent, which will retrieve relevant context from Qdrant and generate a response grounded in the book content.

**Request**:
- **Method**: POST
- **Path**: `/agent/query`
- **Content-Type**: `application/json`
- **Authentication**: None

**Request Schema**:
```json
{
  "type": "object",
  "required": ["query"],
  "properties": {
    "query": {
      "type": "string",
      "description": "The natural language query from the user",
      "minLength": 1,
      "maxLength": 1000,
      "example": "What are the key principles of RAG systems?"
    },
    "scope": {
      "type": "string",
      "enum": ["full_book", "selected_text"],
      "default": "full_book",
      "description": "Query scope - full book or selected text only",
      "example": "full_book"
    },
    "scope_filters": {
      "type": "object",
      "properties": {
        "urls": {
          "type": "array",
          "items": {
            "type": "string",
            "format": "uri"
          },
          "description": "Specific URLs to search within",
          "example": ["https://book.example.com/chapter1"]
        },
        "modules": {
          "type": "array",
          "items": {
            "type": "string"
          },
          "description": "Specific modules to search within",
          "example": ["introduction", "advanced-topics"]
        },
        "sections": {
          "type": "array",
          "items": {
            "type": "string"
          },
          "description": "Specific sections to search within",
          "example": ["section-1.1", "section-2.3"]
        }
      },
      "description": "Metadata filters for selected_text scope"
    },
    "max_results": {
      "type": "integer",
      "minimum": 1,
      "maximum": 20,
      "default": 5,
      "description": "Maximum number of results to retrieve",
      "example": 5
    },
    "min_similarity": {
      "type": "number",
      "minimum": 0.0,
      "maximum": 1.0,
      "default": 0.5,
      "description": "Minimum similarity threshold for results",
      "example": 0.7
    }
  }
}
```

**Response**:
- **Success Response**: `200 OK`
- **Error Responses**: `400 Bad Request`, `422 Validation Error`, `500 Internal Server Error`

**Success Response Schema**:
```json
{
  "type": "object",
  "required": ["response", "sources", "confidence", "query_time", "retrieved_chunks_count"],
  "properties": {
    "response": {
      "type": "string",
      "description": "The agent's response to the query",
      "example": "RAG systems combine retrieval and generation to provide contextually relevant responses..."
    },
    "sources": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["content", "source_url", "source_title", "similarity_score", "metadata", "chunk_id"],
        "properties": {
          "content": {
            "type": "string",
            "description": "The content of the retrieved chunk",
            "example": "Retrieval-Augmented Generation (RAG) is a technique that combines..."
          },
          "source_url": {
            "type": "string",
            "format": "uri",
            "description": "URL of the source document",
            "example": "https://book.example.com/chapter1"
          },
          "source_title": {
            "type": "string",
            "description": "Title of the source document",
            "example": "Introduction to RAG Systems"
          },
          "similarity_score": {
            "type": "number",
            "minimum": 0.0,
            "maximum": 1.0,
            "description": "Similarity score of this chunk",
            "example": 0.85
          },
          "metadata": {
            "type": "object",
            "description": "Additional metadata about the source",
            "example": {"module": "introduction", "section": "section-1.1"}
          },
          "chunk_id": {
            "type": "string",
            "description": "Unique identifier for this chunk",
            "example": "https://book.example.com/chapter1#100-500"
          }
        }
      },
      "description": "List of sources used in the response"
    },
    "confidence": {
      "type": "number",
      "minimum": 0.0,
      "maximum": 1.0,
      "description": "Overall confidence level of the response",
      "example": 0.92
    },
    "query_time": {
      "type": "number",
      "description": "Time taken to process the query in seconds",
      "example": 1.23
    },
    "retrieved_chunks_count": {
      "type": "integer",
      "description": "Number of chunks retrieved from vector store",
      "example": 3
    }
  }
}
```

**Error Responses**:
- `400 Bad Request`: Invalid request parameters
- `422 Validation Error`: Request validation failed
- `500 Internal Server Error`: Server error during processing

**Example Request**:
```json
{
  "query": "Explain how RAG systems work in detail",
  "scope": "selected_text",
  "scope_filters": {
    "modules": ["architecture", "implementation"],
    "sections": ["section-3.1", "section-3.2"]
  },
  "max_results": 3,
  "min_similarity": 0.6
}
```

**Example Response**:
```json
{
  "response": "RAG systems work by first retrieving relevant documents or passages from a knowledge base based on the user query, then using these retrieved documents as context to generate a response. This two-step process allows the system to ground its responses in factual information from the knowledge base.",
  "sources": [
    {
      "content": "Retrieval-Augmented Generation (RAG) is a technique that combines information retrieval with text generation...",
      "source_url": "https://book.example.com/chapter3",
      "source_title": "RAG Architecture",
      "similarity_score": 0.87,
      "metadata": {"module": "architecture", "section": "section-3.1"},
      "chunk_id": "https://book.example.com/chapter3#200-600"
    }
  ],
  "confidence": 0.94,
  "query_time": 1.45,
  "retrieved_chunks_count": 1
}
```

### GET /health
Health check endpoint to verify the service is running.

**Description**: Simple endpoint to check if the service is operational.

**Request**:
- **Method**: GET
- **Path**: `/health`
- **Authentication**: None

**Response**:
- **Success Response**: `200 OK`
```json
{
  "status": "healthy",
  "timestamp": "2025-12-23T10:30:00Z"
}
```

### GET /docs
OpenAPI documentation endpoint (auto-generated by FastAPI).

**Description**: Interactive API documentation using Swagger UI.

**Request**:
- **Method**: GET
- **Path**: `/docs`
- **Authentication**: None

## Integration Patterns

### Request Flow
1. Client sends query to `/agent/query` endpoint
2. Request validated against schema
3. Query processed by RAG agent
4. Context retrieved from Qdrant based on scope
5. OpenAI agent generates response using context
6. Response formatted with source citations
7. Response returned to client

### Error Handling
- Validation errors return 422 with detailed error messages
- API connectivity issues return 500 with appropriate messages
- Query processing timeouts return 500 with timeout indication

### Performance Considerations
- Responses should be returned within 5 seconds for 90% of requests
- Maximum 20 results per query to prevent context window overflow
- Similarity threshold helps filter irrelevant results