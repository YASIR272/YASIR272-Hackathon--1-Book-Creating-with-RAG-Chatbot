# Quickstart Guide: Module 1 – The Robotic Nervous System (ROS 2)

**Feature**: 001-ros2-module
**Date**: 2025-12-16

## Overview

This quickstart guide provides the essential steps to set up and begin working with Module 1 of the ROS 2 book for AI developers.

## Prerequisites

- Node.js LTS (v18 or higher)
- npm package manager
- Basic understanding of JavaScript/Markdown
- Git for version control

## Setup Instructions

### 1. Initialize Docusaurus Project

```bash
# Create a new Docusaurus project
npx create-docusaurus@latest my-ros2-book classic

# Navigate to project directory
cd my-ros2-book
```

### 2. Install Required Dependencies

```bash
# Install additional dependencies if needed
npm install
```

### 3. Create Module 1 Structure

```bash
# Create module directory
mkdir -p docs/module1

# Create the three required chapters
touch docs/module1/index.md
touch docs/module1/chapter1-fundamentals.md
touch docs/module1/chapter2-python-agents.md
touch docs/module1/chapter3-urdf.md
```

### 4. Configure Sidebar Navigation

Update `sidebars.js` to include Module 1:

```javascript
// sidebars.js
module.exports = {
  tutorialSidebar: [
    'intro',
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
  ],
};
```

### 5. Add Module Content

Create the content for each chapter:

**docs/module1/index.md**:
```markdown
---
sidebar_position: 1
---

# Module 1: The Robotic Nervous System (ROS 2)

Welcome to Module 1, where you'll learn the fundamentals of ROS 2 as the nervous system of robots. This module covers:
- Core ROS 2 architecture concepts
- Python agents with rclpy
- Humanoid robot description with URDF

By the end of this module, you'll understand how AI algorithms connect to robot control systems.
```

### 6. Run Development Server

```bash
npm run start
```

Your Docusaurus site will be available at http://localhost:3000

### 7. Build for Production

```bash
npm run build
```

## Key Configuration Files

### Docusaurus Configuration
The `docusaurus.config.js` file should be configured with:
- Site title and description
- Theme customization
- Plugin configurations
- Deployment settings for GitHub Pages

### Content Structure
- All book content goes in the `docs/` directory
- Modules are organized in subdirectories (e.g., `docs/module1/`)
- Each chapter is a separate MDX file
- Navigation is controlled through `sidebars.js`

## Deployment to GitHub Pages

1. Configure the `deployment` settings in `docusaurus.config.js`
2. Set up GitHub Actions workflow for automatic deployment
3. Push changes to the main branch to trigger deployment

## Next Steps

After completing this quickstart:
1. Develop the content for each of the three chapters
2. Add practical examples and code snippets
3. Implement the concept-first explanations as specified
4. Test the navigation and user experience
5. Prepare for deployment to GitHub Pages