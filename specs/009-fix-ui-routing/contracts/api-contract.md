# API Contract: Fixed RAG Chatbot Integration

## Overview
This document defines the API contract for the repaired RAG backend integration with the Docusaurus frontend. The API enables users to submit queries about book content, send selected text as context, and receive responses from the RAG system. This contract includes fixes for proper content retrieval and context handling.

## Base URL
`http://localhost:8000/api/v1` (for local development)
`https://[deployment-url]/api/v1` (for production)

## Content Type
All requests and responses use `application/json` content type.

## Endpoints

### POST /chat/query
Submit a user query to the RAG system with optional selected text context. This endpoint now properly retrieves content from the book and handles selected text context correctly.

#### Request
```json
{
  "query": "What is the main concept discussed in this section?",
  "selectedText": "Optional selected text that provides context for the query",
  "sessionId": "unique-session-identifier"
}
```

#### Request Validation
- `query` (string, required): Must be 1-1000 characters
- `selectedText` (string, optional): Up to 5000 characters
- `sessionId` (string, required): Valid session identifier

#### Response - 200 OK
```json
{
  "id": "response-unique-id",
  "queryId": "query-unique-id",
  "answer": "The main concept discussed is based on the actual book content...",
  "sources": [
    {
      "documentId": "doc-123",
      "section": "Chapter 1: Introduction",
      "pageUrl": "/docs/intro",
      "text": "The main concept is from the actual book content...",
      "confidence": 0.95
    }
  ],
  "timestamp": "2025-12-24T10:00:00Z",
  "sessionId": "unique-session-identifier"
}
```

#### Response - 400 Bad Request
```json
{
  "error": "Invalid request parameters",
  "details": {
    "query": "Query must be between 1 and 1000 characters"
  }
}
```

#### Response - 500 Internal Server Error
```json
{
  "error": "Backend service unavailable",
  "details": "Unable to process query at this time"
}
```

### GET /chat/session/{sessionId}
Retrieve session information and query history.

#### Response - 200 OK
```json
{
  "sessionId": "unique-session-identifier",
  "startTime": "2025-12-24T09:00:00Z",
  "lastActivity": "2025-12-24T10:00:00Z",
  "queryHistory": [
    {
      "queryId": "query-1",
      "timestamp": "2025-12-24T09:30:00Z",
      "queryText": "What is the main concept?",
      "responseId": "response-1"
    }
  ],
  "activeContext": {}
}
```

### POST /chat/validate
Validate the connection to the RAG backend service.

#### Response - 200 OK
```json
{
  "status": "available",
  "message": "RAG backend is ready to process queries",
  "timestamp": "2025-12-24T10:00:00Z"
}
```

### GET /chat/search
Search the book content for specific terms. This is a new endpoint to support better content discovery.

#### Query Parameters
- `q` (string, required): Search query
- `limit` (integer, optional): Number of results to return (default: 10, max: 50)
- `sessionId` (string, optional): Session identifier

#### Response - 200 OK
```json
{
  "query": "search term",
  "results": [
    {
      "documentId": "doc-123",
      "section": "Chapter Title",
      "pageUrl": "/docs/chapter",
      "contentPreview": "Preview of the content that matches the search...",
      "score": 0.95
    }
  ],
  "totalResults": 15,
  "timestamp": "2025-12-24T10:00:00Z"
}
```

## Error Handling
- 400: Client error due to invalid request parameters
- 404: Requested resource not found
- 500: Server error or backend service unavailable
- 503: Service temporarily unavailable, try again later

## Security
- Rate limiting applied per IP address (30 requests per minute)
- Input validation applied to prevent injection attacks
- Session-based tracking for query history and context

## Performance Expectations
- API response times under 5 seconds for 90% of requests
- Search results returned within 2 seconds
- Proper error handling during high load periods