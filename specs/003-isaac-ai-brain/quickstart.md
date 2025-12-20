# Quickstart Guide: Module 3 – The AI-Robot Brain (NVIDIA Isaac™)

**Feature**: 003-isaac-ai-brain
**Date**: 2025-12-16

## Overview

This quickstart guide provides the essential steps to set up and begin working with Module 3 of the simulation book for AI developers advancing into perception and navigation for humanoid robots. This module covers NVIDIA Isaac Sim, Isaac ROS & VSLAM, and Nav2 path planning.

## Prerequisites

- Node.js LTS (v18 or higher) - for Docusaurus documentation
- NVIDIA Isaac Sim (latest stable release) - for photorealistic simulation
- Isaac ROS packages - for hardware-accelerated perception
- Nav2 (Navigation2) - for path planning with ROS2
- Compatible NVIDIA GPU (RTX series recommended) - for accelerated rendering
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

### 2. Create Module 3 Structure

```bash
# Create module directory if not already created
mkdir -p docs/module3

# Create the three required chapters
touch docs/module3/index.md
touch docs/module3/chapter1-isaac-sim-basics.md
touch docs/module3/chapter2-isaac-ros-vslam.md
touch docs/module3/chapter3-path-planning-nav2.md
```

### 3. Update Sidebar Navigation

Ensure the sidebar.js file includes Module 3 entries:

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
    {
      type: 'category',
      label: 'Module 3: The AI-Robot Brain (NVIDIA Isaac™)',
      items: [
        'module3/index',
        'module3/chapter1-isaac-sim-basics',
        'module3/chapter2-isaac-ros-vslam',
        'module3/chapter3-path-planning-nav2',
      ],
    },
  ],
};
```

### 4. Add Module 3 Content

Create the content for each chapter:

**docs/module3/index.md**:
```markdown
---
sidebar_position: 1
---

# Module 3: The AI-Robot Brain (NVIDIA Isaac™)

Welcome to Module 3, where you'll learn about creating AI-driven humanoid robots using NVIDIA Isaac Sim for perception and navigation. This module covers:

- Photorealistic simulation with Isaac Sim
- Hardware-accelerated visual SLAM and perception pipelines
- Path planning with Nav2 for bipedal humanoid motion

By the end of this module, you'll understand how to implement perception, navigation, and AI-driven control systems for humanoid robots.
```

### 5. Isaac Sim Environment Setup

1. Install NVIDIA Isaac Sim from the official NVIDIA Omniverse launcher
2. Verify installation: `isaac-sim --version` (if command available)
3. Test with a simple scene: Launch Isaac Sim and load a sample environment

### 6. Isaac ROS Integration Setup

1. Install Isaac ROS packages following the official documentation
2. Set up ROS2 environment with Isaac ROS extensions
3. Verify perception pipeline functionality

### 7. Nav2 Path Planning Setup

1. Install Navigation2 packages for ROS2
2. Configure for humanoid robot kinematics
3. Test basic navigation in simulation

### 8. Run Development Server

```bash
# From the frontend_book directory
npm run start
```

Your Docusaurus site will be available at http://localhost:3000 with Module 3 content.

## Key Configuration Files

### Docusaurus Configuration
The `docusaurus.config.js` file should already be configured for the existing project structure.

### Content Structure
- All book content goes in the `docs/` directory
- Modules are organized in subdirectories (e.g., `docs/module3/`)
- Each chapter is a separate MDX file
- Navigation is controlled through `sidebars.js`

### Module 3 Specific Setup

#### Isaac Sim Configuration
- USD scene files (.usd, .usda) for environment setup
- Robot models in USD format
- Sensor configurations for cameras, LiDAR, and IMU simulation

#### Perception Pipeline Configuration
- ROS2 launch files for perception nodes
- Parameter configurations for visual SLAM algorithms
- Sensor calibration files

#### Navigation Configuration
- Costmap configurations for Nav2
- Robot footprint definitions for bipedal motion
- Controller configurations for humanoid-specific locomotion

## Next Steps

After completing this quickstart:
1. Develop the content for each of the three chapters
2. Add practical examples and simulation configurations
3. Implement the hands-on instructions as specified
4. Test the navigation and user experience
5. Prepare for advanced AI perception techniques