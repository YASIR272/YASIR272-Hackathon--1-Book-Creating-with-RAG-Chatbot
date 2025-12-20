# API Contracts: Module 3 – The AI-Robot Brain (NVIDIA Isaac™)

**Feature**: 003-isaac-ai-brain
**Date**: 2025-12-16

## Overview

This document defines the API contracts for the backend services that may be needed to support the Docusaurus-based book, particularly for the RAG chatbot integration mentioned in the constitution. These APIs would specifically support Isaac Sim, VSLAM, and navigation content for Module 3.

## Isaac Sim Content Retrieval API

### GET /api/content/module3/{chapterId}

**Purpose**: Retrieve content from Module 3 chapters for the RAG system

**Parameters**:
- chapterId (string, required): Identifier for the specific chapter

**Response**:
- 200 OK: Content retrieved successfully
  - content (string): The chapter content in plain text format
  - metadata (object): Chapter metadata including title, concepts covered
- 404 Not Found: Chapter does not exist

**Example Request**:
```
GET /api/content/module3/chapter1-isaac-sim-basics
```

**Example Response**:
```json
{
  "content": "Full text content of the Isaac Sim basics chapter...",
  "metadata": {
    "title": "NVIDIA Isaac Sim Basics",
    "concepts": ["photorealistic simulation", "synthetic data generation", "environment setup"],
    "lastUpdated": "2025-12-16"
  }
}
```

## Perception Pipeline API

### GET /api/perception/config/{type}

**Purpose**: Retrieve perception pipeline configuration examples for Isaac ROS & VSLAM

**Parameters**:
- type (string, required): Type of configuration ('vslam', 'feature-detection', 'tracking', 'mapping')

**Response**:
- 200 OK: Configuration retrieved successfully
  - config (string): Configuration file content (JSON, YAML, etc.)
  - description (string): Explanation of the configuration
  - examples (array): Multiple examples if applicable

**Example Request**:
```
GET /api/perception/config/vslam
```

**Example Response**:
```json
{
  "config": "yaml configuration content...",
  "description": "VSLAM configuration for Isaac ROS with hardware acceleration",
  "examples": [
    {
      "name": "Basic VSLAM setup",
      "config": "yaml configuration..."
    }
  ]
}
```

## Navigation Configuration API

### GET /api/navigation/config/{type}

**Purpose**: Retrieve navigation configuration examples for Nav2 path planning

**Parameters**:
- type (string, required): Type of configuration ('costmap', 'planner', 'controller', 'behavior-tree')

**Response**:
- 200 OK: Configuration retrieved successfully
  - config (string): Configuration file content (YAML, etc.)
  - description (string): Explanation of the configuration
  - examples (array): Multiple examples if applicable

**Example Request**:
```
GET /api/navigation/config/controller
```

**Example Response**:
```json
{
  "config": "yaml controller configuration...",
  "description": "Controller configuration for bipedal humanoid motion",
  "examples": [
    {
      "name": "Humanoid motion controller",
      "config": "yaml configuration..."
    }
  ]
}
```

## Search API

### POST /api/search

**Purpose**: Search across Module 3 content for the RAG chatbot

**Request Body**:
- query (string, required): Search query from user
- context (string, optional): Context to narrow search scope (e.g., "isaac-sim", "vslam", "nav2")

**Response**:
- 200 OK: Search completed successfully
  - results (array): Array of search results with relevance scores
  - context (string): Relevant content snippets

**Example Request**:
```json
{
  "query": "How to set up photorealistic simulation in Isaac Sim?",
  "context": "module3"
}
```

**Example Response**:
```json
{
  "results": [
    {
      "title": "NVIDIA Isaac Sim Basics",
      "content": "To set up photorealistic simulation in Isaac Sim, you need to configure the RTX renderer and set up proper lighting conditions...",
      "relevance": 0.95,
      "source": "/docs/module3/chapter1-isaac-sim-basics"
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
  - concepts (array): List of key concepts covered in the module

**Example Response**:
```json
{
  "modules": [
    {
      "id": "module3",
      "title": "The AI-Robot Brain (NVIDIA Isaac™)",
      "description": "Perception and navigation for humanoid robots using NVIDIA Isaac platform",
      "chapters": 3,
      "estimatedDuration": "6 hours"
    }
  ],
  "chapters": [
    {
      "id": "chapter1-isaac-sim-basics",
      "moduleId": "module3",
      "title": "NVIDIA Isaac Sim Basics",
      "concepts": ["photorealistic simulation", "synthetic data generation", "environment setup"],
      "prerequisites": ["basic ROS2 knowledge"]
    }
  ],
  "concepts": [
    {
      "name": "Visual SLAM",
      "relatedChapters": ["chapter2-isaac-ros-vslam"],
      "description": "Simultaneous Localization and Mapping using visual sensors"
    }
  ]
}
```