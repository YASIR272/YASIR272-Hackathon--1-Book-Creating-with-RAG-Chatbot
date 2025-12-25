# Data Model: RAG Backend-Frontend Integration

## Entities

### User Query
- **Fields**:
  - `id`: string (unique identifier for the query)
  - `text`: string (the actual query text from the user)
  - `selectedText`: string (optional selected text context)
  - `timestamp`: datetime (when the query was submitted)
  - `sessionId`: string (session identifier for maintaining conversation context)

- **Validation Rules**:
  - `text` must be non-empty and less than 1000 characters
  - `selectedText` can be empty or up to 5000 characters
  - `timestamp` is automatically generated
  - `sessionId` must be a valid session identifier

### RAG Response
- **Fields**:
  - `id`: string (unique identifier for the response)
  - `queryId`: string (reference to the original query)
  - `answer`: string (the generated answer from the RAG system)
  - `sources`: array of SourceReference objects (citations to book content)
  - `timestamp`: datetime (when the response was generated)
  - `sessionId`: string (session identifier for maintaining conversation context)

- **Validation Rules**:
  - `answer` must be non-empty
  - `sources` must be an array of valid SourceReference objects
  - `timestamp` is automatically generated

### SourceReference
- **Fields**:
  - `documentId`: string (identifier for the source document)
  - `section`: string (section title or heading)
  - `pageUrl`: string (URL to the page containing the source)
  - `text`: string (the actual text that was referenced)
  - `confidence`: number (confidence score of the reference, 0-1)

- **Validation Rules**:
  - `documentId`, `section`, `pageUrl`, and `text` must be non-empty
  - `confidence` must be between 0 and 1

### API Communication Layer
- **Fields**:
  - `requestId`: string (unique identifier for the API request)
  - `endpoint`: string (the API endpoint being called)
  - `method`: string (HTTP method: GET, POST, etc.)
  - `requestPayload`: object (the data sent in the request)
  - `responsePayload`: object (the data received in response)
  - `status`: number (HTTP status code)
  - `timestamp`: datetime (when the request was made)
  - `duration`: number (time taken for the request in milliseconds)

- **Validation Rules**:
  - `endpoint` must be a valid API endpoint
  - `method` must be a valid HTTP method
  - `status` must be a valid HTTP status code

### Session Context
- **Fields**:
  - `sessionId`: string (unique identifier for the session)
  - `startTime`: datetime (when the session started)
  - `lastActivity`: datetime (when the last activity occurred)
  - `queryHistory`: array of QueryHistoryItem objects (history of queries in the session)
  - `activeContext`: object (current context for the session)

- **Validation Rules**:
  - `sessionId` must be unique
  - `startTime` and `lastActivity` are automatically managed
  - `queryHistory` must be an array of valid QueryHistoryItem objects

### QueryHistoryItem
- **Fields**:
  - `queryId`: string (reference to the original query)
  - `timestamp`: datetime (when the query was made)
  - `queryText`: string (the original query text)
  - `responseId`: string (reference to the response, if any)

- **Validation Rules**:
  - `queryId` and `responseId` must be valid identifiers
  - `timestamp` is automatically generated
  - `queryText` must be non-empty