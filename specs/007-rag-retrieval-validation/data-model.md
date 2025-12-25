# Data Model: RAG Retrieval Validation

## Entity: QueryRequest
**Description**: Represents a user query with optional metadata filters
**Attributes**:
- query_text: string (required) - The original text query from the user
- metadata_filters: dict (optional) - Key-value pairs for filtering (URL, module, section, etc.)
- top_k: integer (default: 5) - Number of top results to return
- similarity_threshold: float (optional) - Minimum similarity score for results

## Entity: RetrievedChunk
**Description**: A text chunk retrieved from the vector database
**Attributes**:
- content: string (required) - The actual text content of the chunk
- similarity_score: float (required) - Cosine similarity score to the query
- source_url: string (required) - URL of the original document
- source_title: string (required) - Title of the original document
- metadata: dict (required) - Additional metadata (module, section, etc.)
- confidence_score: float (required) - Confidence in the relevance of this chunk

## Entity: RetrievalResult
**Description**: The complete result of a retrieval operation
**Attributes**:
- query_request: QueryRequest (required) - The original request that generated this result
- retrieved_chunks: list of RetrievedChunk (required) - List of chunks returned
- execution_time: float (required) - Time taken to execute the retrieval in seconds
- total_chunks_found: integer (required) - Total number of chunks that matched before top-k selection
- search_params: dict (required) - Parameters used for the similarity search

## Entity: MetadataFilter
**Description**: Criteria used to filter search results by metadata attributes
**Attributes**:
- field_name: string (required) - Name of the metadata field to filter on
- operator: string (required) - Filter operation (equals, contains, in, etc.)
- value: string|list (required) - Value(s) to match against
- case_sensitive: boolean (default: false) - Whether the filter is case sensitive

## Entity: ValidationResult
**Description**: Result of a validation test against expected answers
**Attributes**:
- query: string (required) - The test query
- expected_answers: list of string (required) - Expected relevant answers
- retrieved_chunks: list of RetrievedChunk (required) - Chunks returned by the system
- accuracy_score: float (required) - Score measuring how well results match expectations
- validation_passed: boolean (required) - Whether the validation met the threshold
- detailed_feedback: string (optional) - Detailed feedback about the validation result