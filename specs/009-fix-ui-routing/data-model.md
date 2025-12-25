# Data Model: Fix UI Routing Issues and Repair RAG Chatbot

## Entities

### Navigation State
- **Fields**:
  - `currentPage`: string (the current page URL)
  - `navigationHistory`: array of NavigationEntry objects (previous pages visited)
  - `sidebarState`: object (expanded/collapsed state of sidebar items)
  - `timestamp`: datetime (when the state was last updated)

- **Validation Rules**:
  - `currentPage` must be a valid URL within the site
  - `navigationHistory` must be an array of valid NavigationEntry objects
  - `sidebarState` must be a valid state object

### NavigationEntry
- **Fields**:
  - `url`: string (the page URL)
  - `title`: string (the page title)
  - `timestamp`: datetime (when the entry was added)

- **Validation Rules**:
  - `url` must be a valid internal URL
  - `title` must be non-empty

### UI Component State
- **Fields**:
  - `componentId`: string (unique identifier for the component)
  - `isVisible`: boolean (whether the component is currently visible)
  - `position`: object (coordinates for positioning)
  - `properties`: object (component-specific properties)
  - `timestamp`: datetime (when the state was last updated)

- **Validation Rules**:
  - `componentId` must be unique
  - `isVisible` must be a boolean
  - `position` must contain valid coordinates

### API Request Context
- **Fields**:
  - `requestId`: string (unique identifier for the request)
  - `queryText`: string (the original query text)
  - `selectedText`: string (the selected text context, if any)
  - `sessionId`: string (session identifier)
  - `metadata`: object (additional request metadata)
  - `timestamp`: datetime (when the request was made)

- **Validation Rules**:
  - `requestId` must be unique
  - `queryText` must be non-empty and less than 1000 characters
  - `selectedText` can be empty or up to 5000 characters
  - `sessionId` must be valid

### API Response Context
- **Fields**:
  - `responseId`: string (unique identifier for the response)
  - `requestId`: string (reference to the original request)
  - `answerText`: string (the generated answer)
  - `sources`: array of SourceReference objects (citations to book content)
  - `confidenceScores`: object (confidence scores for different aspects)
  - `timestamp`: datetime (when the response was generated)

- **Validation Rules**:
  - `responseId` must be unique
  - `requestId` must reference a valid request
  - `answerText` must be non-empty
  - `sources` must be an array of valid SourceReference objects

### Cleanup Task
- **Fields**:
  - `taskId`: string (unique identifier for the cleanup task)
  - `taskType`: string (type of cleanup: "unused-file", "deprecated-code", etc.)
  - `targetPath`: string (path to the item to be cleaned up)
  - `status`: string (current status: "pending", "completed", "failed")
  - `timestamp`: datetime (when the task was created)

- **Validation Rules**:
  - `taskId` must be unique
  - `taskType` must be a valid cleanup type
  - `targetPath` must be a valid file or directory path
  - `status` must be one of the allowed values