---
sidebar_position: 4
---

# Humanoid Description with URDF

## Learning Objectives

By the end of this chapter, you will be able to:
- Understand the structure and purpose of URDF in robot description
- Identify and explain the different types of links and joints in URDF
- Describe how sensors are represented in URDF
- Explain how URDF maps to software control mechanisms
- Interpret a URDF file and understand its robot structure

## Introduction to URDF and its Role in Robot Description

Unified Robot Description Format (URDF) is an XML-based format used in ROS to describe robot models. It defines the physical and visual properties of a robot, including links, joints, and other components. URDF serves as the bridge between the physical robot and its digital representation in software.

### Key Concepts of URDF

URDF enables:
- **Physical modeling**: Accurate representation of robot geometry and physics
- **Visualization**: Proper display of robot models in tools like RViz
- **Simulation**: Physics simulation in Gazebo and other simulators
- **Control mapping**: Connection between high-level commands and joint control

## Links: The Building Blocks of Robot Structure

Links represent rigid bodies in the robot. Each link has physical properties like mass, inertia, visual representation, and collision properties. Links are the building blocks of a robot's structure and don't move relative to themselves.

### Link Properties

A link definition includes several important elements:

- **Visual**: How the link appears in visualization tools
- **Collision**: How the link interacts with other objects in simulation
- **Inertial**: Mass, center of mass, and inertia tensor for physics simulation

### Example Link Definition

```xml
<link name="link_name">
  <visual>
    <geometry>
      <cylinder length="0.6" radius="0.1"/>
    </geometry>
    <material name="blue">
      <color rgba="0 0 0.8 1"/>
    </material>
  </visual>
  <collision>
    <geometry>
      <cylinder length="0.6" radius="0.1"/>
    </geometry>
  </collision>
  <inertial>
    <mass value="1"/>
    <inertia ixx="1.0" ixy="0.0" ixz="0.0" iyy="1.0" iyz="0.0" izz="1.0"/>
  </inertial>
</link>
```

## Joints: Connecting Robot Parts

Joints define the connection between links and specify how they can move relative to each other. Different joint types allow different kinds of motion: revolute joints for rotation, prismatic joints for linear motion, continuous joints for unlimited rotation, and fixed joints for rigid connections.

### Joint Types and Applications

The main joint types include:

- **Revolute**: Rotational joint with limited range (like an elbow)
- **Continuous**: Rotational joint with unlimited range (like a wheel)
- **Prismatic**: Linear joint with limited range (like a linear actuator)
- **Fixed**: Rigid connection (no movement)
- **Floating**: 6-DOF connection (for base of floating robots)
- **Planar**: Movement in a plane

### Example Joint Definition

```xml
<joint name="joint_name" type="revolute">
  <parent link="parent_link"/>
  <child link="child_link"/>
  <origin xyz="0 0 1" rpy="0 0 0"/>
  <axis xyz="0 0 1"/>
  <limit lower="-1.57" upper="1.57" effort="100" velocity="1"/>
</joint>
```

## Sensors in URDF

URDF can also describe sensors attached to the robot, such as cameras, IMUs, and LiDARs. Sensor definitions specify their position and orientation relative to links, enabling simulation of sensor data.

### Sensor Integration

Sensors in URDF are typically represented as additional links connected with fixed joints to the parts of the robot where they're mounted. This allows proper positioning and orientation in the robot model.

### Example Sensor Definition

```xml
<link name="camera_link">
  <visual>
    <geometry>
      <box size="0.02 0.08 0.04"/>
    </geometry>
  </visual>
</link>

<joint name="camera_joint" type="fixed">
  <parent link="head_link"/>
  <child link="camera_link"/>
  <origin xyz="0.05 0 0.1" rpy="0 0 0"/>
</joint>
```

## Mapping URDF to Software Control

The URDF description directly maps to the software control architecture. The kinematic chain defined by joints and links determines how control commands are transformed from task space to joint space, enabling precise robot control.

### Forward and Inverse Kinematics

URDF provides the necessary information for:
- **Forward Kinematics**: Calculating end-effector position from joint angles
- **Inverse Kinematics**: Calculating joint angles for desired end-effector position

These are essential for robot control and are used in trajectory planning and motion control.

### Joint Control Mapping

The joint names and types defined in URDF directly correspond to:
- Joint state messages in ROS
- Joint command topics for control
- Kinematic solvers for motion planning

## Practical Example: URDF for a Simple Humanoid Robot

A simple humanoid robot URDF would include:

**Links:**
- base_link (robot base/root)
- torso
- head
- left_upper_arm, left_lower_arm, left_hand
- right_upper_arm, right_lower_arm, right_hand
- left_upper_leg, left_lower_leg, left_foot
- right_upper_leg, right_lower_leg, right_foot

**Joints:**
- Fixed joint connecting base_link to torso
- Revolute joints for shoulders, elbows, hips, knees
- Fixed joints for hands and feet

This structure creates a kinematic chain that enables the robot to move and interact with its environment.

### Understanding URDF Structure

When reading a URDF file, look for:
1. The base link (root of the kinematic tree)
2. The chain of links and joints that form the robot structure
3. The joint types and their limits
4. The sensor placements
5. The physical properties of each link

## Concept-First Approach to URDF

When working with URDF, focus on understanding:

- **Kinematic structure**: How links and joints form the robot's movement capabilities
- **Physical properties**: How mass and inertia affect robot behavior
- **Coordinate systems**: How origins and axes define spatial relationships
- **Control mapping**: How URDF connects to actual robot control

## Summary

URDF provides the essential bridge between the physical robot structure and its software representation. Understanding URDF enables you to work with robot models and develop control algorithms that properly interact with the robot's physical structure.

You now understand:
- How links form the basic structure of robot models
- How joints define movement between links
- How sensors are integrated into the robot model
- How URDF maps to software control mechanisms

## Next Steps

This completes Module 1, where you've learned about ROS 2 fundamentals, how to create Python agents with rclpy, and how humanoid robots are described with URDF. This foundation prepares you for Module 2 on simulation.