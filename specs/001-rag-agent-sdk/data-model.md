# Data Model: RAG-Enabled Agent with OpenAI SDK and FastAPI

## Overview
This document defines the data models for the RAG-enabled agent system, including request/response models and internal data structures.

## API Request/Response Models

### AgentQueryRequest
Represents a query request to the RAG agent.

**Fields**:
- `query` (string, required): The natural language query from the user
- `scope` (string, optional): Query scope - "full_book" (default) or "selected_text"
- `scope_filters` (object, optional): Metadata filters for selected_text scope
  - `urls` (array of strings, optional): Specific URLs to search within
  - `modules` (array of strings, optional): Specific modules to search within
  - `sections` (array of strings, optional): Specific sections to search within
- `max_results` (integer, optional): Maximum number of results to retrieve (default: 5)
- `min_similarity` (number, optional): Minimum similarity threshold (default: 0.5)

**Validation**:
- Query must be non-empty and less than 1000 characters
- Scope must be one of "full_book", "selected_text"
- Max_results must be between 1 and 20
- Min_similarity must be between 0.0 and 1.0

### AgentQueryResponse
Represents the response from the RAG agent.

**Fields**:
- `response` (string, required): The agent's response to the query
- `sources` (array of SourceReference, required): List of sources used in the response
- `confidence` (number, required): Overall confidence level (0.0 to 1.0)
- `query_time` (number, required): Time taken to process the query in seconds
- `retrieved_chunks_count` (integer, required): Number of chunks retrieved from vector store

### SourceReference
Represents a reference to a source document used in the response.

**Fields**:
- `content` (string, required): The content of the retrieved chunk
- `source_url` (string, required): URL of the source document
- `source_title` (string, required): Title of the source document
- `similarity_score` (number, required): Similarity score of this chunk (0.0 to 1.0)
- `metadata` (object, required): Additional metadata about the source
- `chunk_id` (string, required): Unique identifier for this chunk

## Internal Data Models

### AgentQuery
Internal model representing a query being processed by the agent.

**Fields**:
- `query_text` (string, required): The original query text
- `scope_filters` (object, optional): Applied scope filters
- `retrieved_context` (array of RetrievedChunk, required): Context retrieved from Qdrant
- `agent_response` (string, required): Raw response from the OpenAI agent
- `processed_response` (string, required): Response with citations and formatting applied
- `execution_time` (number, required): Total execution time

### RetrievedChunk
Represents a chunk of content retrieved from the vector store.

**Fields**:
- `id` (string, required): Unique identifier for the chunk
- `content` (string, required): The text content of the chunk
- `similarity_score` (number, required): Similarity score from vector search
- `source_url` (string, required): URL of the source document
- `source_title` (string, required): Title of the source document
- `metadata` (object, required): Additional metadata from the source
- `vector_embedding` (array of numbers, optional): The vector embedding (not returned in API)

## State Transitions

### Query Processing Flow
1. **Received**: Query request validated and accepted
2. **Retrieving**: Context being retrieved from Qdrant based on scope
3. **Processing**: OpenAI agent processing retrieved context
4. **Formatting**: Response being formatted with citations
5. **Completed**: Response ready for return to client

## Relationships

- AgentQueryRequest → (processed by) → AgentQuery
- AgentQuery → (contains) → multiple RetrievedChunk
- AgentQuery → (produces) → AgentQueryResponse
- AgentQueryResponse → (contains) → multiple SourceReference
- SourceReference → (references) → RetrievedChunk