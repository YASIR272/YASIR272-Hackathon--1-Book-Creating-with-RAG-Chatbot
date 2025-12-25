import React, { useState, useEffect } from 'react';
import QueryInput from './QueryInput';
import ResponseDisplay from './ResponseDisplay';
import TextSelectionUtil from '../../../static/js/text-selection';
import ragApiClient from '../../services/api-client';
import ErrorBoundary from './ErrorBoundary';
import './rag-chatbot.css';

const Chatbot = ({ pageContext }) => {
  const [sessionId, setSessionId] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [conversation, setConversation] = useState([]);
  const [selectedText, setSelectedText] = useState('');

  // Initialize session
  useEffect(() => {
    // Try to get session ID from local storage, or generate a new one
    const storedSessionId = localStorage.getItem('ragChatbotSessionId');
    const newSessionId = storedSessionId || ragApiClient.generateSessionId();

    if (!storedSessionId) {
      localStorage.setItem('ragChatbotSessionId', newSessionId);
    }

    setSessionId(newSessionId);

    // Validate connection to backend
    validateConnection();
  }, []);

  // Validate connection to backend
  const validateConnection = async () => {
    try {
      await ragApiClient.validateConnection();
    } catch (err) {
      setError('Backend service unavailable. Please ensure the RAG backend is running on port 8000.');
    }
  };

  // Handle query submission
  const handleQuerySubmit = async (queryText, contextSelectedText = null) => {
    if (!queryText.trim()) return;

    setIsLoading(true);
    setError(null);

    try {
      // Use the selected text passed from QueryInput component, or fallback to current selection
      const currentSelectedText = contextSelectedText || TextSelectionUtil.getSelectedText() || selectedText;

      // Add user query to conversation
      const userMessage = { id: Date.now(), type: 'user', content: queryText, timestamp: new Date() };
      setConversation(prev => [...prev, userMessage]);

      // Submit query to backend
      const response = await ragApiClient.submitQuery(queryText, currentSelectedText, sessionId);

      // Add bot response to conversation
      const botMessage = {
        id: response.id,
        type: 'bot',
        content: response.answer,
        sources: response.sources || [],
        timestamp: new Date()
      };
      setConversation(prev => [...prev, botMessage]);

      // Clear selected text after use
      setSelectedText('');
    } catch (err) {
      setError(`Error submitting query: ${err.message}`);
    } finally {
      setIsLoading(false);
    }
  };

  // Handle text selection
  const handleTextSelection = () => {
    const selected = TextSelectionUtil.getSelectedText();
    if (selected) {
      setSelectedText(selected);
      TextSelectionUtil.highlightSelection();
    }
  };

  // Set up text selection event listener
  useEffect(() => {
    const handleSelection = () => {
      handleTextSelection();
    };

    document.addEventListener('mouseup', handleSelection);
    return () => {
      document.removeEventListener('mouseup', handleSelection);
    };
  }, []);

  return (
    <ErrorBoundary>
      <div className="rag-chatbot-container" role="main" aria-label="RAG Chatbot Interface">
        <div className="rag-chatbot-header" role="banner">
          <h3>RAG Chatbot</h3>
          {error && <div className="rag-error-message" role="alert" aria-live="polite">{error}</div>}
        </div>

        <div className="rag-conversation-area" role="log" aria-live="polite" aria-label="Conversation history">
          {conversation.length === 0 ? (
            <div className="rag-welcome-message" role="status" aria-live="polite">
              <p>Ask questions about this book's content. Select text to provide context for your questions.</p>
            </div>
          ) : (
            conversation.map((message) => (
              <div key={message.id} className={`rag-message rag-message-${message.type}`} role="listitem" aria-label={`${message.type} message`}>
                <div className="rag-message-content">
                  {message.type === 'user' ? (
                    <span className="rag-user-icon" aria-label="User">👤</span>
                  ) : (
                    <span className="rag-bot-icon" aria-label="Bot">🤖</span>
                  )}
                  <div className="rag-message-text">
                    {message.content}
                    {message.sources && message.sources.length > 0 && (
                      <div className="rag-sources">
                        <details>
                          <summary aria-label="Toggle sources visibility">Sources</summary>
                          {message.sources.map((source, index) => (
                            <div key={index} className="rag-source-item">
                              <a href={source.page_url} target="_blank" rel="noopener noreferrer" aria-label={`Source: ${source.section}`}>
                                {source.section}
                              </a>
                              <span className="rag-confidence" aria-label={`Confidence: ${(source.confidence * 100).toFixed(1)}%`}>
                                ({(source.confidence * 100).toFixed(1)}%)
                              </span>
                            </div>
                          ))}
                        </details>
                      </div>
                    )}
                  </div>
                </div>
              </div>
            ))
          )}

          {isLoading && (
            <div className="rag-loading-indicator" role="status" aria-live="polite">
              <span>Thinking...</span>
            </div>
          )}
        </div>

        <QueryInput
          onSubmit={handleQuerySubmit}
          isLoading={isLoading}
          selectedText={selectedText}
          ariaLabel="Query input field"
        />
      </div>
    </ErrorBoundary>
  );
};

export default Chatbot;