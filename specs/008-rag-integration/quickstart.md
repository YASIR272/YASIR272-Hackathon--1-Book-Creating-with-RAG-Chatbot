# Quickstart Guide: RAG Backend-Frontend Integration

## Prerequisites
- Node.js 18+ for Docusaurus frontend
- Python 3.11+ for FastAPI backend
- Git for version control
- Basic knowledge of React and JavaScript

## Setup Instructions

### 1. Clone and Prepare the Repository
```bash
# You should already have the repository
cd E:\Hackathon Complete Project 1 Booking Creation
```

### 2. Start the Backend Service
```bash
# Navigate to the backend directory (create if it doesn't exist)
cd backend_rag_pipeline

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies (if requirements.txt exists)
pip install -r requirements.txt

# Or install required packages
pip install fastapi uvicorn

# Start the backend service
uvicorn src.main:app --host 0.0.0.0 --port 8000
```

### 3. Run the Frontend Development Server
```bash
# Navigate to the frontend directory
cd frontend_book

# Install dependencies
npm install

# Start the Docusaurus development server
npm run start
```

### 4. Verify Integration
- Open your browser to `http://localhost:3000`
- Navigate to any documentation page
- You should see the RAG chatbot component
- Test the query functionality to ensure it connects to the backend

## Key Components

### Frontend Components
- `RAGChatbot/Chatbot.jsx` - Main chatbot component
- `RAGChatbot/QueryInput.jsx` - Input component for user queries
- `RAGChatbot/ResponseDisplay.jsx` - Component to display responses
- `services/api-client.js` - API client for backend communication
- `static/js/text-selection.js` - Text selection functionality

### Backend Endpoints
- `POST /api/v1/chat/query` - Submit user queries
- `GET /api/v1/chat/session/{sessionId}` - Get session information
- `POST /api/v1/chat/validate` - Validate backend service

## Testing the Integration
1. Submit a simple query from the frontend
2. Verify that the query is sent to the backend
3. Check that a response is received and displayed
4. Test with selected text context
5. Verify error handling when backend is unavailable

## Troubleshooting
- If the backend is not responding, ensure it's running on port 8000
- Check browser console for frontend errors
- Verify CORS settings if running on different ports
- Confirm that API endpoints match the contract specification