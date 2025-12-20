# Quickstart Guide: Module 2 – The Digital Twin (Gazebo & Unity)

**Feature**: 002-digital-twin
**Date**: 2025-12-16

## Overview

This quickstart guide provides the essential steps to set up and begin working with Module 2 of the simulation book for AI developers. This module covers physics simulation in Gazebo, high-fidelity rendering in Unity, and digital twin integration.

## Prerequisites

- Node.js LTS (v18 or higher) - for Docusaurus documentation
- Gazebo Classic (v11.x or later) - for physics simulation
- Unity Hub with Unity 2022.3 LTS or later - for visual rendering
- Basic understanding of JavaScript/Markdown
- Git for version control

## Setup Instructions

### 1. Verify Docusaurus Project

```bash
# Navigate to the project directory
cd frontend_book

# Install dependencies if not already done
npm install

# Verify the project runs
npm start
```

### 2. Create Module 2 Structure

```bash
# Create module directory if not already created
mkdir -p docs/module2

# Create the three required chapters
touch docs/module2/index.md
touch docs/module2/chapter1-physics-simulation.md
touch docs/module2/chapter2-high-fidelity-rendering.md
touch docs/module2/chapter3-digital-twin-integration.md
```

### 3. Update Sidebar Navigation

Ensure the sidebar.js file includes Module 2 entries (this should already be done from the specification phase):

```javascript
// sidebars.js
module.exports = {
  tutorialSidebar: [
    {
      type: 'category',
      label: 'Module 1: The Robotic Nervous System (ROS 2)',
      items: [
        'module1/index',
        'module1/chapter1-fundamentals',
        'module1/chapter2-python-agents',
        'module1/chapter3-urdf',
      ],
    },
    {
      type: 'category',
      label: 'Module 2: The Digital Twin (Gazebo & Unity)',
      items: [
        'module2/index',
        'module2/chapter1-physics-simulation',
        'module2/chapter2-high-fidelity-rendering',
        'module2/chapter3-digital-twin-integration',
      ],
    },
  ],
};
```

### 4. Add Module 2 Content

Create the content for each chapter:

**docs/module2/index.md**:
```markdown
---
sidebar_position: 1
---

# Module 2: The Digital Twin (Gazebo & Unity)

Welcome to Module 2, where you'll learn about creating digital twins using Gazebo for physics simulation and Unity for high-fidelity visualization. This module covers:

- Physics simulation in Gazebo with gravity, collisions, and sensor simulation
- High-fidelity rendering in Unity for human-robot interaction
- Digital twin integration to synchronize physics and visual representations

By the end of this module, you'll understand how to create comprehensive simulation environments for testing AI agents.
```

### 5. Gazebo Environment Setup

1. Install Gazebo Classic from the official website or package manager
2. Verify installation: `gazebo --version`
3. Test with a simple world: `gazebo worlds/empty.world`

### 6. Unity Environment Setup

1. Install Unity Hub from the official website
2. Install Unity 2022.3 LTS or later through Unity Hub
3. Create a new 3D project to verify installation

### 7. Run Development Server

```bash
# From the frontend_book directory
npm run start
```

Your Docusaurus site will be available at http://localhost:3000 with Module 2 content.

## Key Configuration Files

### Docusaurus Configuration
The `docusaurus.config.js` file should already be configured for the existing project structure.

### Content Structure
- All book content goes in the `docs/` directory
- Modules are organized in subdirectories (e.g., `docs/module2/`)
- Each chapter is a separate MDX file
- Navigation is controlled through `sidebars.js`

## Module 2 Specific Setup

### Physics Simulation (Chapter 1)
- Gazebo world files (.world) for environment setup
- Robot models in URDF/SDF format
- Sensor configurations for LiDAR, IMU, and depth cameras

### Visual Rendering (Chapter 2)
- Unity scene files (.unity) for 3D environments
- Material and texture assets
- Lighting and camera configurations

### Digital Twin Integration (Chapter 3)
- Communication protocols between Gazebo and Unity
- State synchronization mechanisms
- Data validation and verification methods

## Next Steps

After completing this quickstart:
1. Develop the content for each of the three chapters
2. Add practical examples and simulation configurations
3. Implement the hands-on instructions as specified
4. Test the navigation and user experience
5. Prepare for Module 3 (Advanced AI perception)