---
sidebar_position: 2
---

# ROS 2 Fundamentals for Physical AI

## Learning Objectives

By the end of this chapter, you will be able to:
- Explain what ROS 2 is and its role as robot middleware
- Describe the differences between nodes, topics, services, and actions
- Understand how these components work together in a robot system
- Identify appropriate use cases for each communication pattern

## Introduction to ROS 2 as Robot Middleware

Robot Operating System 2 (ROS 2) is not an operating system but rather a middleware framework that provides services designed for a heterogeneous computer cluster. It includes hardware abstraction, device drivers, libraries, visualizers, message-passing, package management, and more.

ROS 2 serves as the "nervous system" of a robot, enabling different components to communicate with each other seamlessly. As an AI developer, understanding ROS 2 architecture is crucial for connecting your AI algorithms to physical robot systems.

### Key Concepts of Middleware

Middleware acts as a bridge between applications and the underlying operating system, providing a standardized way for different software components to communicate. In robotics, this allows for:

- **Modularity**: Components can be developed and tested independently
- **Flexibility**: Different programming languages and platforms can interoperate
- **Scalability**: Systems can grow without requiring complete rewrites

## Nodes: The Foundation of ROS 2

Nodes are the fundamental building blocks of a ROS 2 system. Each node is a process that performs computation and communicates with other nodes through messages. Nodes can be written in different programming languages and run on different machines, yet they can still communicate with each other.

### Characteristics of Nodes

- **Process-based**: Each node runs as a separate process
- **Unique naming**: Each node must have a unique name within the ROS 2 domain
- **Communication hub**: Nodes interact with other nodes via topics, services, and actions
- **Language agnostic**: Nodes can be written in different languages (C++, Python, etc.)

### Creating a Node

In ROS 2, nodes are created by inheriting from the `Node` class provided by the client library (rclpy for Python, rclcpp for C++, etc.). Each node must have a unique name within the ROS 2 domain.

### Example Node Structure

```
MyRobotNode
├── Publishers (for sending data)
├── Subscribers (for receiving data)
├── Services (for request/response)
├── Actions (for goal-oriented tasks)
└── Internal logic (AI algorithms, etc.)
```

## Topics: Asynchronous Communication

Topics are named buses over which nodes exchange messages. Topics implement a many-to-many relationship where multiple nodes can publish to the same topic and multiple nodes can subscribe to the same topic. This enables decoupled, asynchronous communication between nodes.

### Key Features of Topics

- **Publish/Subscribe pattern**: Asynchronous communication
- **Decoupling**: Publishers and subscribers don't need to know about each other
- **Many-to-many**: Multiple publishers and subscribers can exist for the same topic
- **Data-driven**: Communication happens when data is available

### Publisher-Subscriber Pattern

The publisher-subscriber pattern allows nodes to send and receive messages without having direct knowledge of each other. Publishers send messages to topics without knowing who will receive them, and subscribers receive messages from topics without knowing who sent them.

### Quality of Service (QoS)

ROS 2 provides Quality of Service settings that allow you to control how messages are delivered, including reliability, durability, and history policies.

## Services: Synchronous Request-Response

Services provide a request-response communication pattern, implementing a many-to-one relationship where multiple clients can make requests to a single service server. Services are synchronous, meaning the client waits for a response before continuing execution.

### Key Features of Services

- **Request/Response pattern**: Synchronous communication
- **Many-to-one**: Multiple clients can call one service
- **Blocking**: Client waits for response before continuing
- **Stateless**: Each request is independent

### When to Use Services

Services are appropriate when you need a guaranteed response to a request, such as:
- Requesting current sensor data
- Commanding an action that should return status
- Configuring parameters
- Performing validation tasks

## Actions: Advanced Goal-Oriented Communication

Actions are a more advanced communication pattern that extends services with feedback and goal management. They're designed for long-running tasks that may take significant time to complete, providing status updates during execution and allowing for cancellation.

### Action Components

Actions consist of three message types:
- **Goal**: The request (what to do)
- **Result**: The response (outcome of the task)
- **Feedback**: Intermediate updates (progress during execution)

### When to Use Actions

Actions are ideal for tasks like:
- Navigation to a destination
- Trajectory execution
- Calibration procedures
- Any long-running task requiring progress monitoring

## Practical Example: How These Components Work Together

Let's consider a mobile robot performing a delivery task:

1. **Nodes**:
   - Navigation node (handles movement)
   - Perception node (detects obstacles)
   - Task manager node (coordinates the delivery)

2. **Topics**:
   - `/scan` - LIDAR data published by perception node
   - `/cmd_vel` - Velocity commands published by navigation node
   - `/battery_status` - Battery information published by power system

3. **Services**:
   - `/get_map` - Service to request the current map
   - `/set_initial_pose` - Service to set the robot's initial position

4. **Actions**:
   - `/navigate_to_pose` - Action to move to a specific location with feedback

This example shows how the different communication patterns work together to enable complex robot behavior.

## Concept-First Approach

As emphasized throughout this book, we focus on understanding concepts before implementation details. The key concepts you should understand from this chapter are:

- **Decoupling**: Components communicate without direct dependencies
- **Abstraction**: Complex robot systems are broken into manageable parts
- **Flexibility**: Different communication patterns for different needs
- **Scalability**: Systems can grow without complete rewrites

## Summary

Understanding these fundamental ROS 2 concepts is essential for developing AI systems that interact with physical robots. The decoupled nature of ROS 2 communication allows for flexible, modular robot architectures where AI algorithms can be developed independently and integrated with various robot platforms.

You now understand the core components of ROS 2:
- Nodes as the fundamental execution units
- Topics for asynchronous, decoupled communication
- Services for synchronous request-response interactions
- Actions for long-running, goal-oriented tasks

## Next Steps

In the next chapter, we'll explore how to create Python agents that communicate with ROS controllers using rclpy, bridging your AI logic to robot control systems.