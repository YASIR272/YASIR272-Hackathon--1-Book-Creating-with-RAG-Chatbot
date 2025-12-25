# Research: RAG-Enabled Agent with OpenAI SDK and FastAPI

## Overview
This document captures research findings for implementing a RAG-enabled agent using OpenAI Agents SDK and FastAPI, integrated with Qdrant vector database for book content retrieval.

## Key Decisions and Rationale

### 1. OpenAI Agent Architecture
**Decision**: Use OpenAI Assistant API with custom retrieval tools
**Rationale**: The Assistant API provides built-in RAG capabilities and can be enhanced with custom tools to interface with Qdrant
**Alternatives considered**:
- OpenAI Functions API (more manual control but less built-in RAG)
- LangChain agents (higher abstraction but less direct control)

### 2. Qdrant Integration Approach
**Decision**: Create custom retrieval tools that query Qdrant directly
**Rationale**: Allows precise control over retrieval parameters and metadata filtering for scoped queries
**Alternatives considered**:
- Using OpenAI's built-in vector store (less flexible for custom metadata filtering)
- Pinecone integration (already committed to Qdrant in constitution)

### 3. FastAPI Endpoint Design
**Decision**: RESTful API with structured request/response models
**Rationale**: Provides clear contract for integration, supports async operations for better performance
**Alternatives considered**:
- GraphQL (more complex for simple RAG use case)

### 4. Query Scoping Implementation
**Decision**: Use metadata filtering in Qdrant queries to support full-book vs. selected-text modes
**Rationale**: Leverages Qdrant's native filtering capabilities efficiently
**Alternatives considered**:
- Separate collections per book section (more complex management)

## Technical Research Findings

### OpenAI Agents SDK Integration
- OpenAI Assistant API supports custom tools that can be used to interface with Qdrant
- Assistant can maintain conversation context and use tool results to generate responses
- Requires OpenAI API key and proper Assistant setup

### Qdrant Retrieval Patterns
- Qdrant supports metadata filtering which is perfect for scoped queries
- Can filter by URL, module, section, or custom metadata fields
- Cosine similarity search provides relevant results for semantic queries

### FastAPI Async Patterns
- FastAPI naturally supports async operations which is important for external API calls
- Pydantic models provide excellent request/response validation
- Built-in OpenAPI documentation generation

## Implementation Approach

### Agent-Service Architecture
1. FastAPI receives user query
2. Agent service creates/retrieves OpenAI Assistant
3. Custom tool queries Qdrant with retrieval logic
4. Assistant processes tool results and generates response
5. Response includes citations and confidence levels

### Scoped Query Support
- Full-book queries: No metadata filters applied
- Selected-text queries: Apply metadata filters based on scope parameters
- Metadata stored during indexing phase (from existing RAG pipeline) will support this

## Risks and Mitigations

### API Rate Limits
- Risk: OpenAI and Qdrant API rate limits
- Mitigation: Implement caching and proper rate limiting on our end

### Response Time
- Risk: Multiple external API calls could cause slow responses
- Mitigation: Async operations and potential caching layer

### Context Window Limits
- Risk: Large retrieval results may exceed context window
- Mitigation: Implement result summarization and top-k limiting