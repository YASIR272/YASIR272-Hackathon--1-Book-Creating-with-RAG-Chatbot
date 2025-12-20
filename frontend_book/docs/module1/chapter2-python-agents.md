---
sidebar_position: 3
---

# Python Agents with rclpy

## Learning Objectives

By the end of this chapter, you will be able to:
- Understand the role of rclpy as the Python client library for ROS 2
- Create ROS 2 nodes using Python
- Implement publishers and subscribers with rclpy
- Design message passing patterns that bridge AI logic to robot control
- Apply rclpy concepts to practical robot control scenarios

## Introduction to rclpy and its Role in ROS 2

rclpy is the Python client library for ROS 2, providing a Python API to interact with the ROS 2 middleware. It allows Python developers to create nodes, publish and subscribe to topics, provide and use services, and work with actions. As an AI developer, rclpy is your bridge between Python-based AI algorithms and ROS 2-based robot control systems.

### Why Python for AI Integration

Python is the dominant language in AI development, with extensive libraries for machine learning, computer vision, and data processing. rclpy enables seamless integration between these Python-based AI tools and ROS 2 robot systems.

## Creating Nodes with rclpy

To create a node in Python using rclpy, you need to import the ROS 2 Python client library and create a class that inherits from `rclpy.node.Node`. The node class should initialize the parent Node class with a unique node name.

### Basic Node Structure

A basic ROS 2 node in Python follows a standard structure:

```python
import rclpy
from rclpy.node import Node

class MyPythonAgentNode(Node):
    def __init__(self):
        super().__init__('my_python_agent')
        # Initialize publishers, subscribers, services, etc.

def main(args=None):
    rclpy.init(args=args)
    node = MyPythonAgentNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
```

### Node Initialization Best Practices

When creating nodes with rclpy:
- Use descriptive node names that indicate the node's function
- Initialize all publishers, subscribers, and services in the `__init__` method
- Handle proper cleanup in the node's destruction
- Consider using parameters for configuration

## Publishers in rclpy

Publishers allow nodes to send messages to topics. To create a publisher, you call the `create_publisher()` method on your node, specifying the message type and topic name. The publisher can then send messages using the `publish()` method.

### Creating a Publisher

```python
from std_msgs.msg import String

class MyPublisherNode(Node):
    def __init__(self):
        super().__init__('publisher_node')
        self.publisher = self.create_publisher(String, 'my_topic', 10)
        self.timer = self.create_timer(0.5, self.timer_callback)  # Publish every 0.5 seconds

    def timer_callback(self):
        msg = String()
        msg.data = 'Hello from Python agent!'
        self.publisher.publish(msg)
        self.get_logger().info(f'Publishing: {msg.data}')
```

### Example Publisher Implementation

A publisher node might collect data from an AI algorithm and publish it to a topic for other nodes to consume. This enables the AI logic to communicate with other parts of the robot system.

### Publisher Best Practices

- Set appropriate queue sizes based on your application's needs
- Use timers for periodic publishing when appropriate
- Consider Quality of Service (QoS) settings for reliability
- Log important publishing events for debugging

## Subscribers in rclpy

Subscribers allow nodes to receive messages from topics. To create a subscriber, you call the `create_subscription()` method, specifying the message type, topic name, and a callback function to handle incoming messages.

### Creating a Subscriber

```python
from std_msgs.msg import String

class MySubscriberNode(Node):
    def __init__(self):
        super().__init__('subscriber_node')
        self.subscription = self.create_subscription(
            String,
            'my_topic',
            self.listener_callback,
            10)  # Queue size
        self.subscription  # Prevent unused variable warning

    def listener_callback(self, msg):
        self.get_logger().info(f'I heard: {msg.data}')
        # Process the received message with AI logic
```

### Example Subscriber Implementation

A subscriber node might receive sensor data from the robot and process it with AI algorithms. The callback function processes each message as it arrives, enabling real-time interaction with the robot.

### Subscriber Best Practices

- Design callback functions to be lightweight and fast
- Use appropriate queue sizes to handle message bursts
- Consider threading for computationally expensive processing
- Handle message types safely with proper validation

## Message Passing Concepts

Message passing in ROS 2 is the fundamental communication mechanism between nodes. Messages are serialized data structures that conform to specific message definitions (`.msg` files). The middleware handles the delivery of messages between publishers and subscribers.

### Message Types

ROS 2 provides standard message types for common data:
- `std_msgs`: Basic data types (Int, Float, String, etc.)
- `geometry_msgs`: Geometric primitives (Point, Pose, Vector3, etc.)
- `sensor_msgs`: Sensor data formats (LaserScan, Image, JointState, etc.)
- `nav_msgs`: Navigation-related messages (Odometry, Path, etc.)

### Custom Message Types

You can also define custom message types for your specific application needs, following the `.msg` file format.

## Practical Example: Bridging AI Logic to Robot Control

Let's consider a practical example where an AI algorithm makes decisions based on sensor input and sends commands to the robot. The AI node subscribes to sensor topics and publishes to actuator command topics, creating a complete bridge between AI logic and robot control.

### AI Decision Node Implementation

```python
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist

class AIDecisionNode(Node):
    def __init__(self):
        super().__init__('ai_decision_node')

        # Subscribe to sensor data
        self.subscription = self.create_subscription(
            LaserScan,
            '/scan',
            self.scan_callback,
            10)

        # Publish to robot velocity commands
        self.publisher = self.create_publisher(Twist, '/cmd_vel', 10)

        # AI state variables
        self.obstacle_detected = False

    def scan_callback(self, msg):
        # Simple AI logic: detect obstacles in front of robot
        front_range = min(msg.ranges[0:10] + msg.ranges[-10:])  # Front 20 degrees

        cmd_msg = Twist()

        if front_range < 1.0:  # Obstacle within 1 meter
            # Stop and turn
            cmd_msg.linear.x = 0.0
            cmd_msg.angular.z = 0.5  # Turn right
        else:
            # Move forward
            cmd_msg.linear.x = 0.2
            cmd_msg.angular.z = 0.0

        self.publisher.publish(cmd_msg)
```

This example demonstrates how AI logic (obstacle avoidance) connects to robot control through message passing.

## Concept-First Approach to Python Agents

When developing Python agents with rclpy, focus on understanding the conceptual patterns first:

- **Separation of Concerns**: Keep AI logic separate from ROS communication
- **Asynchronous Processing**: Design for non-blocking message handling
- **State Management**: Maintain node state appropriately for robot control
- **Error Handling**: Design robust error handling for real-world robot applications

## Summary

Using rclpy, you can seamlessly integrate your Python-based AI algorithms with ROS 2 robot systems. The publisher-subscriber pattern enables asynchronous, decoupled communication that fits well with many AI architectures. You now understand how to:

- Create nodes with proper initialization and cleanup
- Implement publishers and subscribers
- Design message passing patterns for AI-robot integration
- Apply these concepts to practical robot control scenarios

## Next Steps

In the next chapter, we'll explore how humanoid robots are described using URDF, and how this description maps to software control mechanisms.