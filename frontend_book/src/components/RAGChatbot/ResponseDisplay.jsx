import React from 'react';

const ResponseDisplay = ({ response, isLoading, error }) => {
  if (isLoading) {
    return (
      <div className="rag-response-display rag-loading">
        <div className="rag-loading-content">
          <div className="rag-loading-dots">
            <span>.</span>
            <span>.</span>
            <span>.</span>
          </div>
          <p>Processing your query...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="rag-response-display rag-error">
        <div className="rag-error-content">
          <h4>Error</h4>
          <p>{error}</p>
        </div>
      </div>
    );
  }

  if (!response) {
    return (
      <div className="rag-response-display rag-empty">
        <p>Ask a question to see the response here.</p>
      </div>
    );
  }

  return (
    <div className="rag-response-display rag-loaded" role="region" aria-label="Response display">
      <div className="rag-response-content">
        <div className="rag-answer">
          <h4>Response:</h4>
          <p aria-label="Response text">{response.answer}</p>
        </div>

        {response.sources && response.sources.length > 0 && (
          <div className="rag-sources-section" role="region" aria-label="Sources and citations">
            <h4>Sources:</h4>
            <ul className="rag-sources-list" role="list">
              {response.sources.map((source, index) => (
                <li key={index} className="rag-source-item" role="listitem">
                  <div className="rag-source-details">
                    <a href={source.page_url} target="_blank" rel="noopener noreferrer" aria-label={`Source: ${source.section}`}>
                      {source.section}
                    </a>
                    <div className="rag-source-text" aria-label={`Source text preview: ${source.text.substring(0, 100)}${source.text.length > 100 ? '...' : ''}`}>
                      "{source.text.substring(0, 100)}{source.text.length > 100 ? '...' : ''}"
                    </div>
                    <div className="rag-confidence" aria-label={`Confidence level: ${(source.confidence * 100).toFixed(1)}%`}>
                      <span>Confidence:</span>
                      <span className="rag-confidence-value" aria-hidden="true">{(source.confidence * 100).toFixed(1)}%</span>
                      <div className="rag-confidence-bar" role="progressbar" aria-valuenow={source.confidence * 100} aria-valuemin="0" aria-valuemax="100">
                        <div
                          className="rag-confidence-fill"
                          style={{ width: `${source.confidence * 100}%` }}
                        ></div>
                      </div>
                    </div>
                  </div>
                </li>
              ))}
            </ul>
          </div>
        )}
      </div>
    </div>
  );
};

export default ResponseDisplay;