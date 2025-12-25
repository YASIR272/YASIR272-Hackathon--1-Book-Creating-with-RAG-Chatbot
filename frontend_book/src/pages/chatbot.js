import React from 'react';
import Layout from '@theme/Layout';
import Chatbot from '../components/RAGChatbot/Chatbot';

export default function ChatbotPage() {
  return (
    <Layout title="RAG Chatbot">
      <div style={{
        maxWidth: '800px',
        margin: '0 auto',
        padding: '20px',
        fontFamily: 'Arial, sans-serif'
      }}>
        <h1>RAG Chatbot for Physical AI & Humanoid Robotics</h1>
        <p>
          This chatbot is integrated with our book content using Retrieval-Augmented Generation (RAG) technology.
          You can ask questions about the book content, and the system will provide answers based on the book's material.
        </p>

        <div style={{
          border: '1px solid #ccc',
          borderRadius: '8px',
          padding: '20px',
          marginTop: '20px',
          backgroundColor: '#fafafa'
        }}>
          <Chatbot />
        </div>

        <div style={{ marginTop: '20px' }}>
          <h3>Features:</h3>
          <ul>
            <li>Ask questions about the book content</li>
            <li>Select text on any page and ask questions about it</li>
            <li>See source citations for all answers</li>
            <li>Get confidence scores for source references</li>
            <li>Maintain conversation context across queries</li>
          </ul>
        </div>
      </div>
    </Layout>
  );
}