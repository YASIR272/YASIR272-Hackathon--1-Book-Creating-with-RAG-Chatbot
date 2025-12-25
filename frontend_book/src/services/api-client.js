// API Client Service for RAG Chatbot Integration
// Handles communication between frontend and backend RAG services

class RAGApiClient {
  constructor(baseURL = 'http://localhost:8000/api/v1') {
    this.baseURL = baseURL;
    this.defaultHeaders = {
      'Content-Type': 'application/json',
    };
  }

  // Submit a query to the RAG backend
  async submitQuery(query, selectedText = null, sessionId = null) {
    try {
      const requestBody = {
        query: query,
        selectedText: selectedText || '',
        sessionId: sessionId || this.generateSessionId(),
      };

      const response = await fetch(`${this.baseURL}/chat/query`, {
        method: 'POST',
        headers: { ...this.defaultHeaders },
        body: JSON.stringify(requestBody),
      });

      if (!response.ok) {
        throw new Error(`API request failed: ${response.status} ${response.statusText}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Error submitting query:', error);
      throw error;
    }
  }

  // Get session information
  async getSession(sessionId) {
    try {
      const response = await fetch(`${this.baseURL}/chat/session/${sessionId}`, {
        method: 'GET',
        headers: { ...this.defaultHeaders },
      });

      if (!response.ok) {
        throw new Error(`Failed to get session: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Error getting session:', error);
      throw error;
    }
  }

  // Validate backend connection
  async validateConnection() {
    try {
      const response = await fetch(`${this.baseURL}/chat/validate`, {
        method: 'POST',
        headers: { ...this.defaultHeaders },
      });

      if (!response.ok) {
        throw new Error(`Connection validation failed: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Error validating connection:', error);
      throw error;
    }
  }

  // Generate a session ID if needed
  generateSessionId() {
    return 'session_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
  }
}

// Export the API client as a singleton instance
const ragApiClient = new RAGApiClient();
export default ragApiClient;