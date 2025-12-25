# API Contract: RAG Chatbot Integration

## Overview
This document defines the API contract for the RAG backend integration with the Docusaurus frontend. The API enables users to submit queries about book content, send selected text as context, and receive responses from the RAG system.

## Base URL
`http://localhost:8000/api/v1` (for local development)

## Content Type
All requests and responses use `application/json` content type.

## Endpoints

### POST /chat/query
Submit a user query to the RAG system with optional selected text context.

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
  "answer": "The main concept discussed is...",
  "sources": [
    {
      "documentId": "doc-123",
      "section": "Chapter 1: Introduction",
      "pageUrl": "/docs/intro",
      "text": "The main concept is...",
      "confidence": 0.95
    }
  ],
  "sessionId": "unique-session-identifier",
  "timestamp": "2025-12-24T10:00:00Z"
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
  ]
}
```

### POST /chat/validate
Validate the connection to the RAG backend service.

#### Response - 200 OK
```json
{
  "status": "available",
  "message": "RAG backend is ready to process queries"
}
```

## Error Handling
- 400: Client error due to invalid request parameters
- 404: Requested resource not found
- 500: Server error or backend service unavailable
- 503: Service temporarily unavailable, try again later

## Security
- No authentication required for local development
- Input validation applied to prevent injection attacks
- Rate limiting applied per IP address in production