# Data Model: Book Content RAG Pipeline

## Entities

### BookContent
**Description**: Represents extracted text from a book page
**Fields**:
- url (string): The source URL of the content
- title (string): The page title
- content (string): The extracted clean text content
- metadata (dict): Additional metadata like headings, sections, etc.

### TextChunk
**Description**: A segment of book content prepared for embedding
**Fields**:
- id (string): Unique identifier for the chunk
- content (string): The text content of the chunk
- source_url (string): Reference to the original page URL
- source_title (string): Reference to the original page title
- section_info (dict): Information about the section this chunk belongs to
- metadata (dict): Additional metadata for the chunk

### VectorEmbedding
**Description**: A numerical representation of a text chunk
**Fields**:
- chunk_id (string): Reference to the source TextChunk
- vector (list[float]): The embedding vector (from Cohere API)
- text_content (string): The original text that was embedded
- metadata (dict): Associated metadata including source information

### SearchResult
**Description**: The output of a query operation
**Fields**:
- chunk_id (string): Reference to the matching TextChunk
- text_content (string): The content of the matching chunk
- similarity_score (float): The similarity score from the vector search
- source_info (dict): Information about the source document

## Relationships

```
BookContent 1..* -> 1..* TextChunk
TextChunk 1..* -> 1..* VectorEmbedding
VectorEmbedding 1..* -> 1..* SearchResult (via search)
```

## Validation Rules

### BookContent
- url must be a valid URL format
- content must not be empty
- title must not be empty

### TextChunk
- content length must be within embedding API limits (typically < 4000 tokens)
- source_url must reference an existing BookContent
- chunk size should be optimized for semantic coherence

### VectorEmbedding
- vector must have consistent dimensions (1024 for Cohere embeddings)
- chunk_id must reference an existing TextChunk
- vector values must be valid floats

## State Transitions

### Content Processing Flow
1. **Raw Content**: Initial state when content is extracted from URL
2. **Chunked**: Content is divided into appropriate segments with metadata
3. **Embedded**: Each chunk receives a vector representation
4. **Stored**: Embeddings are persisted in Qdrant with metadata
5. **Queryable**: Ready for semantic search operations

## Schema for Qdrant Collection (book_embedding)

```json
{
  "id": "unique_chunk_id",
  "vector": [/* embedding vector values */],
  "payload": {
    "text_content": "string",
    "source_url": "string",
    "source_title": "string",
    "section_info": "object",
    "chunk_metadata": "object",
    "created_at": "timestamp"
  }
}
```