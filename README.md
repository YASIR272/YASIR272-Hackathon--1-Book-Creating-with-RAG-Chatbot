# Physical AI & Humanoid Robotics Book with RAG Chatbot

This project combines a comprehensive guide to Physical AI and Humanoid Robotics with an integrated RAG (Retrieval-Augmented Generation) chatbot that can answer questions about the book content.

## Project Structure

- `frontend_book/` - Docusaurus-based documentation site with integrated RAG chatbot
- `backend_rag_pipeline/` - FastAPI backend for RAG processing

## Features

- Complete guide to Physical AI & Humanoid Robotics
- Interactive RAG chatbot that answers questions based on book content
- Text selection functionality to ask questions about specific passages
- Session management for conversation context
- Source citations with confidence scores
- Responsive design for all devices
- Accessibility features

## Running the Project

### Prerequisites

- Node.js 18+ for frontend
- Python 3.11+ for backend
- npm or yarn

### Backend Setup (RAG Service)

1. Navigate to the backend directory:
   ```bash
   cd backend_rag_pipeline
   ```

2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Start the backend service:
   ```bash
   python -m uvicorn src.main:app --host 0.0.0.0 --port 8000
   ```

### Frontend Setup (Docusaurus Book)

1. Navigate to the frontend directory:
   ```bash
   cd frontend_book
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm start
   ```

## Usage

1. Start both the backend and frontend services
2. Access the book at `http://localhost:3000` (or whatever port Docusaurus runs on)
3. Use the "Chatbot" link in the navigation to access the dedicated chatbot page
4. Or use the floating chatbot button on any page to ask questions about the book content
5. Select text on any page and ask questions about it for contextual responses

## API Endpoints

The backend provides the following API endpoints:

- `POST /api/v1/chat/query` - Submit a query to the RAG system
- `GET /api/v1/chat/session/{sessionId}` - Get session information
- `POST /api/v1/chat/validate` - Validate the backend connection

## Components

### Frontend Components

- `RAGChatbot/Chatbot.jsx` - Main chatbot component
- `RAGChatbot/QueryInput.jsx` - Input component for queries
- `RAGChatbot/ResponseDisplay.jsx` - Component to display responses
- `services/api-client.js` - API client for backend communication
- `static/js/text-selection.js` - Text selection utility

### Backend Components

- `src/main.py` - FastAPI application entry point
- `src/api/v1/chat.py` - API endpoints
- `src/services/query_processor.py` - Query processing logic
- `src/models/` - Data models for requests and responses
- `src/middleware/request_validation.py` - Validation and security middleware
- `src/utils/logger.py` - Logging utilities

## Security Features

- Rate limiting to prevent abuse
- Input sanitization to prevent injection attacks
- Proper validation of all requests
- Session management with timeout

## Architecture

The system follows a microservice architecture with:

- Frontend: Docusaurus-based static site with React components
- Backend: FastAPI service with RAG capabilities
- Communication: HTTP/JSON API
- Session Management: Client-side storage with server-side context

## Development

The project was built using Spec-Driven Development methodology with:

- Feature specifications defined upfront
- Implementation plans created before coding
- Task breakdowns for systematic implementation
- Comprehensive testing and validation

## License

This project is licensed under the terms specified in the individual components.