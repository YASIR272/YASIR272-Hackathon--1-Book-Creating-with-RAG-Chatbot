import React, { useState } from 'react';
import OriginalLayout from '@theme-original/Layout';
import Chatbot from '../components/RAGChatbot/Chatbot';

export default function Layout(props) {
  const [showChatbot, setShowChatbot] = useState(false);

  const toggleChatbot = () => {
    setShowChatbot(!showChatbot);
  };

  return (
    <>
      <OriginalLayout {...props}>
        {props.children}

        {/* Chatbot toggle button */}
        <button
          onClick={toggleChatbot}
          style={{
            position: 'fixed',
            bottom: showChatbot ? '520px' : '20px',
            right: '20px',
            zIndex: 1000,
            width: '60px',
            height: '60px',
            borderRadius: '50%',
            backgroundColor: '#1976d2',
            color: 'white',
            border: 'none',
            fontSize: '24px',
            cursor: 'pointer',
            boxShadow: '0 4px 12px rgba(0,0,0,0.15)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center'
          }}
          aria-label={showChatbot ? "Close chatbot" : "Open chatbot"}
        >
          {showChatbot ? '✕' : '💬'}
        </button>

        {/* Chatbot panel */}
        {showChatbot && (
          <div style={{
            position: 'fixed',
            bottom: '20px',
            right: '20px',
            zIndex: 1000,
            width: '350px',
            height: '500px',
            border: '1px solid #ccc',
            borderRadius: '8px',
            boxShadow: '0 4px 12px rgba(0,0,0,0.15)',
            backgroundColor: 'white',
            overflow: 'hidden',
            display: 'flex',
            flexDirection: 'column'
          }}>
            <div style={{
              padding: '10px',
              backgroundColor: '#f5f5f5',
              borderBottom: '1px solid #ddd',
              fontWeight: 'bold',
              display: 'flex',
              justifyContent: 'space-between',
              alignItems: 'center'
            }}>
              <span>RAG Chatbot</span>
              <button
                onClick={toggleChatbot}
                style={{
                  background: 'none',
                  border: 'none',
                  fontSize: '18px',
                  cursor: 'pointer',
                  padding: '0',
                  width: '24px',
                  height: '24px'
                }}
                aria-label="Close chatbot"
              >
                ✕
              </button>
            </div>
            <div style={{ flex: 1, overflow: 'auto' }}>
              <Chatbot />
            </div>
          </div>
        )}
      </OriginalLayout>
    </>
  );
}