# API Contract: RAG Retrieval Validation

## Overview
This document defines the API contract for the RAG retrieval validation system. The API provides endpoints for querying the vector database, validating retrieval accuracy, and testing the retrieval pipeline.

## Base URL
```
https://api.example.com/v1/retrieval-validation
```

## Authentication
All endpoints require authentication using an API key in the header:
```
Authorization: Bearer {API_KEY}
```

## Endpoints

### 1. Query Vector Database
**POST** `/search`

Retrieve semantically relevant text chunks based on a natural language query.

#### Request
```json
{
  "query_text": "string (required) - The natural language query",
  "top_k": "integer (optional, default: 5) - Number of top results to return",
  "similarity_threshold": "float (optional) - Minimum similarity score",
  "metadata_filters": {
    "url": "string (optional) - Filter by specific URL",
    "module": "string (optional) - Filter by specific module",
    "section": "string (optional) - Filter by specific section"
  }
}
```

#### Response
```json
{
  "retrieval_result": {
    "query_request": {
      "query_text": "string",
      "metadata_filters": "object",
      "top_k": "integer",
      "similarity_threshold": "float"
    },
    "retrieved_chunks": [
      {
        "content": "string - The text content of the chunk",
        "similarity_score": "float - Cosine similarity to query",
        "source_url": "string - URL of original document",
        "source_title": "string - Title of original document",
        "metadata": "object - Additional metadata",
        "confidence_score": "float - Confidence in relevance"
      }
    ],
    "execution_time": "float - Time taken in seconds",
    "total_chunks_found": "integer - Total chunks matching before top-k",
    "search_params": "object - Parameters used for search"
  }
}
```

#### HTTP Status Codes
- 200: Success - Valid response with retrieval results
- 400: Bad Request - Invalid query parameters
- 401: Unauthorized - Invalid or missing API key
- 500: Internal Server Error - Error during retrieval

### 2. Validate Retrieval Accuracy
**POST** `/validate`

Validate retrieval accuracy against known query-answer pairs.

#### Request
```json
{
  "validation_queries": [
    {
      "query": "string (required) - The test query",
      "expected_answers": ["string"] (required) - Expected relevant answers
    }
  ],
  "validation_threshold": "float (optional, default: 0.85) - Minimum accuracy threshold"
}
```

#### Response
```json
{
  "validation_results": [
    {
      "query": "string - The test query",
      "expected_answers": ["string"] - Expected relevant answers",
      "retrieved_chunks": [
        {
          "content": "string",
          "similarity_score": "float",
          "source_url": "string",
          "source_title": "string",
          "metadata": "object",
          "confidence_score": "float"
        }
      ],
      "accuracy_score": "float - Score measuring match to expectations",
      "validation_passed": "boolean - Whether validation met threshold",
      "detailed_feedback": "string - Feedback about validation result"
    }
  ],
  "overall_accuracy": "float - Overall accuracy across all queries",
  "total_tests": "integer - Total number of validation tests",
  "passed_tests": "integer - Number of tests that passed"
}
```

#### HTTP Status Codes
- 200: Success - Validation completed with results
- 400: Bad Request - Invalid validation parameters
- 401: Unauthorized - Invalid or missing API key
- 500: Internal Server Error - Error during validation

### 3. Test Retrieval Pipeline
**GET** `/health`

Test the retrieval pipeline and return health status.

#### Response
```json
{
  "status": "string - Health status (healthy, degraded, error)",
  "checks": {
    "qdrant_connection": {
      "status": "string - Connection status",
      "message": "string - Additional info"
    },
    "cohere_api": {
      "status": "string - API status",
      "message": "string - Additional info"
    },
    "response_time": "float - Average response time in ms"
  }
}
```

#### HTTP Status Codes
- 200: Success - Health check completed
- 500: Internal Server Error - One or more services are unavailable

## Error Response Format
All error responses follow this format:
```json
{
  "error": {
    "code": "string - Error code",
    "message": "string - Human-readable error message",
    "details": "object - Additional error details (optional)"
  }
}
```

## Rate Limits
- Queries per minute: 100 requests per minute per API key
- Burst limit: 10 requests