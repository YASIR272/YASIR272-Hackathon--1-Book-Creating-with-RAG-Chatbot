import React, { useState } from 'react';

const QueryInput = ({ onSubmit, isLoading, selectedText, ariaLabel = "Query input field" }) => {
  const [query, setQuery] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (query.trim() && !isLoading) {
      onSubmit(query, selectedText);
      setQuery('');
    }
  };

  return (
    <div className="rag-query-input-container" role="form" aria-label="Query input form">
      {selectedText && (
        <div className="rag-selected-text-preview" role="status" aria-live="polite">
          <small>Selected text: "{selectedText.substring(0, 100)}{selectedText.length > 100 ? '...' : ''}"</small>
        </div>
      )}

      <form onSubmit={handleSubmit} className="rag-query-form">
        <div className="rag-input-group">
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Ask a question about this book's content..."
            disabled={isLoading}
            className="rag-query-input"
            aria-label={ariaLabel}
            role="textbox"
            aria-describedby={selectedText ? "selected-text-preview" : undefined}
          />
          <button
            type="submit"
            disabled={isLoading || !query.trim()}
            className="rag-submit-button"
            aria-label={isLoading ? "Sending query" : "Send query"}
          >
            {isLoading ? 'Sending...' : 'Send'}
          </button>
        </div>
      </form>
    </div>
  );
};

export default QueryInput;