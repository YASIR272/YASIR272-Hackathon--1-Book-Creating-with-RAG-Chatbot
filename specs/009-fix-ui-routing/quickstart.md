# Quickstart Guide: Fix UI Routing Issues and Repair RAG Chatbot

## Prerequisites
- Node.js 18+ for Docusaurus frontend
- Python 3.11+ for FastAPI backend
- Git for version control
- Basic knowledge of React, JavaScript, and Python

## Setup Instructions

### 1. Clone and Prepare the Repository
```bash
# Navigate to the project directory
cd E:\Hackathon Complete Project 1 Booking Creation
```

### 2. Set up the Backend Service
```bash
# Navigate to the backend directory
cd backend_rag_pipeline

# Install dependencies
pip install -r requirements.txt

# Start the backend service
uvicorn src.main:app --host 0.0.0.0 --port 8000
```

### 3. Set up the Frontend Development Server
```bash
# Navigate to the frontend directory
cd frontend_book

# Install dependencies
npm install

# Start the Docusaurus development server
npm run start
```

### 4. Verify the Repaired Functionality
- Open your browser to `http://localhost:3000`
- Navigate through different book chapters using the sidebar
- Verify there are no "Page Not Found" errors
- Test the RAG chatbot by asking questions about book content
- Select text on any page and ask questions about the selected text
- Verify that responses come from actual book content with proper citations

## Key Fixes Implemented

### Navigation Fixes
- Fixed broken links in sidebar navigation
- Corrected page routing issues
- Improved chapter navigation flow
- Added proper error handling for missing pages

### RAG Backend Improvements
- Enhanced document retrieval from book content
- Fixed selected text context passing
- Improved response accuracy based on actual book content
- Added proper source citations with confidence scores

### UI Component Refactoring
- Refactored chatbot components for better performance
- Improved error handling in UI components
- Enhanced user feedback during query processing
- Fixed layout and responsiveness issues

## Testing the Repaired System
1. Navigate to different chapters and verify all links work
2. Submit a query about book content and verify the response is from actual book content
3. Select text on a page and ask a question about it
4. Verify that the response acknowledges the selected text context
5. Check that sources are properly cited with URLs to the relevant book sections
6. Test error handling by submitting invalid queries

## Cleaning Up Unused Files
During the repair process, unused and test files were identified and removed:
- Temporary test files in the backend directory
- Deprecated configuration files
- Unnecessary assets and resources
- Old backup files

## Deployment Preparation
The project is now prepared for deployment to GitHub Pages and Vercel:
- Frontend build process validates successfully
- Backend API endpoints are properly configured
- All dependencies are properly declared
- Configuration files are optimized for deployment

## Troubleshooting
- If navigation links still show "Page Not Found", verify the sidebar configuration in `sidebars.js`
- If the RAG chatbot doesn't respond, ensure the backend service is running on port 8000
- If selected text context isn't working, check the text selection utility in `static/js/text-selection.js`
- For build errors, run `npm run build` in the frontend directory to identify issues