# API Contracts: Module 2 – The Digital Twin (Gazebo & Unity)

**Feature**: 002-digital-twin
**Date**: 2025-12-16

## Overview

This document defines the API contracts for the backend services that may be needed to support the Docusaurus-based book, particularly for the RAG chatbot integration mentioned in the constitution. These APIs would specifically support simulation-related content for Module 2.

## Simulation Content Retrieval API

### GET /api/content/module2/{chapterId}

**Purpose**: Retrieve content from Module 2 chapters for the RAG system

**Parameters**:
- chapterId (string, required): Identifier for the specific chapter

**Response**:
- 200 OK: Content retrieved successfully
  - content (string): The chapter content in plain text format
  - metadata (object): Chapter metadata including title, concepts covered
- 404 Not Found: Chapter does not exist

**Example Request**:
```
GET /api/content/module2/chapter1-physics-simulation
```

**Example Response**:
```json
{
  "content": "Full text content of the physics simulation chapter...",
  "metadata": {
    "title": "Physics Simulation in Gazebo",
    "concepts": ["gravity", "collisions", "environment setup", "sensor simulation"],
    "lastUpdated": "2025-12-16"
  }
}
```

## Simulation Configuration API

### GET /api/simulation/config/{type}

**Purpose**: Retrieve simulation configuration examples for Gazebo or Unity

**Parameters**:
- type (string, required): Type of configuration ('gazebo', 'unity', 'synchronization')

**Response**:
- 200 OK: Configuration retrieved successfully
  - config (string): Configuration file content (XML, JSON, etc.)
  - description (string): Explanation of the configuration
  - examples (array): Multiple examples if applicable

**Example Request**:
```
GET /api/simulation/config/gazebo
```

**Example Response**:
```json
{
  "config": "<sdf version='1.6'>...</sdf>",
  "description": "Gazebo world configuration with physics parameters",
  "examples": [
    {
      "name": "Basic physics world",
      "config": "<sdf version='1.6'>...</sdf>"
    }
  ]
}
```

## Search API

### POST /api/search

**Purpose**: Search across Module 2 content for the RAG chatbot

**Request Body**:
- query (string, required): Search query from user
- context (string, optional): Context to narrow search scope (e.g., "gazebo", "unity", "integration")

**Response**:
- 200 OK: Search completed successfully
  - results (array): Array of search results with relevance scores
  - context (string): Relevant content snippets

**Example Request**:
```json
{
  "query": "How to configure LiDAR sensor in Gazebo?",
  "context": "module2"
}
```

**Example Response**:
```json
{
  "results": [
    {
      "title": "Physics Simulation in Gazebo",
      "content": "To configure a LiDAR sensor in Gazebo, you need to add a ray sensor to your robot model...",
      "relevance": 0.95,
      "source": "/docs/module2/chapter1-physics-simulation"
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
      "id": "module2",
      "title": "The Digital Twin (Gazebo & Unity)",
      "description": "Simulation for AI developers using Gazebo and Unity",
      "chapters": 3,
      "estimatedDuration": "6 hours"
    }
  ],
  "chapters": [
    {
      "id": "chapter1-physics-simulation",
      "moduleId": "module2",
      "title": "Physics Simulation in Gazebo",
      "concepts": ["gravity", "collisions", "environment", "sensors", "LiDAR", "IMU", "Depth Cameras"],
      "prerequisites": ["basic physics concepts"]
    }
  ]
}
```