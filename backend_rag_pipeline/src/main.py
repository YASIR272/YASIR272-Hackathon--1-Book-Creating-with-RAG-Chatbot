"""
Main FastAPI Application for RAG Chatbot Integration
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from .api.v1.chat import router as chat_router
from .models.user_query import UserQuery
from .models.rag_response import RAGResponse


# Create FastAPI app instance
app = FastAPI(
    title="RAG Chatbot API",
    description="API for RAG Chatbot Integration with Docusaurus frontend",
    version="1.0.0",
    openapi_url="/api/v1/openapi.json",
    docs_url="/api/v1/docs",
    redoc_url="/api/v1/redoc"
)

# Add CORS middleware to allow requests from frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
app.include_router(chat_router, prefix="/api/v1", tags=["chat"])

# Root endpoint
@app.get("/")
async def root():
    return {"message": "RAG Chatbot API is running", "version": "1.0.0"}

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": "2025-12-24T10:00:00Z"}


# For local development
if __name__ == "__main__":
    uvicorn.run(
        "src.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )