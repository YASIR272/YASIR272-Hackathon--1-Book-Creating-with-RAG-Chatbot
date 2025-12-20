# API Contracts: Module 1 – The Robotic Nervous System (ROS 2)

**Feature**: 001-ros2-module
**Date**: 2025-12-16

## Overview

This document defines the API contracts for the backend services that may be needed to support the Docusaurus-based book, particularly for the RAG chatbot integration mentioned in the constitution.

## Content Retrieval API

### GET /api/content/module1/{chapterId}

**Purpose**: Retrieve content from Module 1 chapters for the RAG system

**Parameters**:
- chapterId (string, required): Identifier for the specific chapter

**Response**:
- 200 OK: Content retrieved successfully
  - content (string): The chapter content in plain text format
  - metadata (object): Chapter metadata including title, concepts covered
- 404 Not Found: Chapter does not exist

**Example Request**:
```
GET /api/content/module1/chapter1-fundamentals
```

**Example Response**:
```json
{
  "content": "Full text content of the ROS 2 fundamentals chapter...",
  "metadata": {
    "title": "ROS 2 Fundamentals for Physical AI",
    "concepts": ["nodes", "topics", "services", "actions", "middleware"],
    "lastUpdated": "2025-12-16"
  }
}
```

## Search API

### POST /api/search

**Purpose**: Search across Module 1 content for the RAG chatbot

**Request Body**:
- query (string, required): Search query from user
- context (string, optional): Context to narrow search scope

**Response**:
- 200 OK: Search completed successfully
  - results (array): Array of search results with relevance scores
  - context (string): Relevant content snippets

**Example Request**:
```json
{
  "query": "How do ROS 2 nodes communicate?",
  "context": "module1"
}
```

**Example Response**:
```json
{
  "results": [
    {
      "title": "ROS 2 Fundamentals",
      "content": "Nodes in ROS 2 communicate through topics, services, and actions...",
      "relevance": 0.95,
      "source": "/docs/module1/chapter1-fundamentals"
    }
  ]
}
```

## Content Metadata API

### GET /api/content/metadata

**Purpose**: Retrieve metadata about available content for navigation

**Response**:
- 200 OK: Metadata retrieved successfully
  - modules (array): List of available modules
  - chapters (array): List of available chapters with metadata

**Example Response**:
```json
{
  "modules": [
    {
      "id": "module1",
      "title": "The Robotic Nervous System (ROS 2)",
      "description": "Introduction to ROS 2 for AI developers",
      "chapters": 3,
      "estimatedDuration": "4 hours"
    }
  ],
  "chapters": [
    {
      "id": "chapter1-fundamentals",
      "moduleId": "module1",
      "title": "ROS 2 Fundamentals for Physical AI",
      "concepts": ["nodes", "topics", "services", "actions", "middleware"],
      "prerequisites": ["basic Python knowledge"]
    }
  ]
}
```