---
sidebar_position: 4
---

# Chapter 3: Path Planning with Nav2

This chapter covers bipedal humanoid motion, trajectory planning, and AI-driven control using Nav2.

## Learning Objectives

- Understand Nav2 path planning for humanoid robots
- Implement bipedal motion constraints and considerations
- Build trajectory planning algorithms for humanoid locomotion
- Develop AI-driven control systems for navigation
- Execute autonomous navigation with obstacle avoidance

## Table of Contents

1. [Introduction to Nav2 and Path Planning](#introduction-to-nav2-and-path-planning)
2. [Bipedal Motion Constraints](#bipedal-motion-constraints)
3. [Trajectory Planning Algorithms](#trajectory-planning-algorithms)
4. [AI-Driven Control Systems](#ai-driven-control-systems)
5. [Autonomous Navigation Implementation](#autonomous-navigation-implementation)
6. [Practical Examples](#practical-examples)
7. [Summary and Next Steps](#summary-and-next-steps)

## Conceptual Overview

Before diving into the technical implementation, it's important to understand the fundamental concepts behind Nav2 path planning for humanoid robots:

- **Nav2 (Navigation 2)**: The ROS 2 navigation stack that provides path planning, execution, and recovery behaviors for autonomous robots
- **Bipedal Motion Planning**: Path planning that accounts for the unique constraints of two-legged locomotion including balance, step placement, and dynamic stability
- **Trajectory Planning**: Generation of time-parameterized paths that consider robot dynamics, kinematics, and environmental constraints
- **Humanoid Locomotion**: The complex movement patterns required for bipedal robots to walk, turn, and navigate while maintaining balance
- **AI-Driven Control**: Intelligent systems that adapt navigation behavior based on environmental conditions and learned patterns
- **Autonomous Navigation**: Complete self-navigation capabilities that allow humanoid robots to move from one location to another without human intervention

These concepts form the foundation of humanoid robot navigation, enabling robots to plan and execute complex movements while maintaining stability and avoiding obstacles.

## Introduction to Nav2 and Path Planning

Nav2 (Navigation 2) is the next-generation navigation stack for ROS 2 that provides comprehensive path planning and execution capabilities for mobile robots. Unlike its predecessor in ROS 1, Nav2 is designed from the ground up to be more modular, flexible, and robust, making it particularly suitable for complex robots like humanoid platforms.

### Nav2 Architecture Overview

Nav2 is built around a flexible, plugin-based architecture that allows for customization of different navigation components:

```
Goal Request → Behavior Tree → Global Planner → Local Planner → Controller → Robot
   ↓              ↓              ↓              ↓             ↓         ↓
Navigation   Task Planning   Path Planning  Trajectory    Motion   Movement
Service                    Global Path    Local Plan    Control   Execution
```

Each component can be replaced with different implementations based on the specific requirements of the robot platform and application.

### Key Nav2 Components

#### 1. Global Planner
The global planner is responsible for generating a high-level path from the robot's current position to the goal location:

- **A* Algorithm**: Traditional A* for optimal pathfinding in grid maps
- **Dijkstra's Algorithm**: Alternative pathfinding algorithm
- **NavFn**: Gradient-based path planner
- **Custom Planners**: Humanoid-specific planners that consider bipedal constraints

#### 2. Local Planner
The local planner creates short-term trajectories that avoid obstacles and follow the global path:

- **Teb Local Planner**: Timely Elastic Band planner that considers robot dynamics
- **DWB Controller**: Dynamic Window Approach controller for real-time obstacle avoidance
- **MPC Controller**: Model Predictive Control for advanced trajectory optimization

#### 3. Behavior Tree Framework
Nav2 uses behavior trees to orchestrate navigation tasks:

- **Task Planning**: Sequences navigation tasks in a logical order
- **Recovery Behaviors**: Automatic recovery from navigation failures
- **Condition Checking**: Verify conditions before executing navigation actions

### Nav2 for Humanoid Robots

While Nav2 was designed primarily for wheeled robots, it can be adapted for humanoid robots with several key modifications:

- **Footstep Planning**: Generate specific footstep locations for bipedal locomotion
- **Balance Constraints**: Incorporate balance requirements into path planning
- **Step Height/Limitations**: Account for humanoid step capabilities in obstacle avoidance
- **Dynamic Stability**: Consider dynamic stability during navigation execution

### Installation and Setup

To use Nav2 for humanoid robot navigation:

```bash
# Install Nav2 packages
sudo apt update
sudo apt install ros-humble-navigation2 ros-humble-nav2-bringup
sudo apt install ros-humble-nav2-controller ros-humble-nav2-planners
sudo apt install ros-humble-nav2-behaviors ros-humble-nav2-util

# Install additional dependencies for humanoid navigation
sudo apt install ros-humble-robot-state-publisher ros-humble-joint-state-publisher
```

### Basic Nav2 Launch

A basic Nav2 launch for humanoid robots would include:

```xml
<!-- humanoid_nav2.launch.py -->
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.conditions import IfCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare

def generate_launch_description():
    # Launch arguments
    use_sim_time = LaunchConfiguration('use_sim_time')
    params_file = LaunchConfiguration('params_file')

    # Nav2 launch
    nav2_bringup_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            PathJoinSubstitution([
                FindPackageShare('nav2_bringup'),
                'launch',
                'navigation_launch.py'
            ])
        ]),
        launch_arguments={
            'use_sim_time': use_sim_time,
            'params_file': params_file
        }.items()
    )

    return LaunchDescription([
        DeclareLaunchArgument(
            'use_sim_time',
            default_value='false',
            description='Use simulation time if true'
        ),
        DeclareLaunchArgument(
            'params_file',
            default_value=PathJoinSubstitution([
                FindPackageShare('humanoid_nav2_config'),
                'params',
                'humanoid_nav2_params.yaml'
            ]),
            description='Full path to the Nav2 params file'
        ),
        nav2_bringup_launch
    ])
```

## Bipedal Motion Constraints and Considerations

Humanoid robots present unique challenges for path planning due to the fundamental differences between wheeled and bipedal locomotion. Understanding these constraints is crucial for developing effective navigation systems.

### Physical Constraints of Bipedal Locomotion

#### 1. Step Limitations
Humanoid robots have physical limitations on their step capabilities:

- **Maximum Step Length**: The maximum distance between consecutive foot placements
- **Minimum Step Width**: The minimum lateral distance between feet for stability
- **Maximum Step Height**: The maximum vertical step capability over obstacles
- **Step Frequency**: The rate at which steps can be executed

```python
class BipedalConstraints:
    def __init__(self):
        # Physical constraints for humanoid robot
        self.max_step_length = 0.60    # meters
        self.min_step_width = 0.30     # meters
        self.max_step_height = 0.15    # meters
        self.min_step_period = 0.5     # seconds per step
        self.foot_size = (0.2, 0.1)    # length, width in meters
        self.support_polygon = self.calculate_support_polygon()

    def calculate_support_polygon(self):
        """Calculate the support polygon for balance"""
        # Simplified polygon - in reality this would be based on foot positions
        return [
            (-0.1, -0.1),  # Left foot corner 1
            (-0.1, 0.1),   # Left foot corner 2
            (0.1, 0.1),    # Right foot corner 1
            (0.1, -0.1)    # Right foot corner 2
        ]

    def is_step_feasible(self, start_pos, end_pos):
        """Check if a step from start to end position is physically feasible"""
        step_distance = self.calculate_distance(start_pos, end_pos)

        # Check if step is within length limits
        if step_distance > self.max_step_length:
            return False, f"Step too long: {step_distance:.2f}m > {self.max_step_length}m"

        # Check if step is above ground limit
        if abs(end_pos.z - start_pos.z) > self.max_step_height:
            return False, f"Step too high: {abs(end_pos.z - start_pos.z):.2f}m > {self.max_step_height}m"

        return True, "Step feasible"

    def calculate_distance(self, pos1, pos2):
        """Calculate 3D distance between two positions"""
        dx = pos2.x - pos1.x
        dy = pos2.y - pos1.y
        dz = pos2.z - pos1.z
        return (dx*dx + dy*dy + dz*dz)**0.5
```

#### 2. Balance Requirements
Maintaining balance is critical for humanoid robots during navigation:

- **Center of Mass (CoM) Position**: The CoM must remain within the support polygon
- **Zero Moment Point (ZMP)**: The point where the net moment of ground reaction forces is zero
- **Stability Margins**: Safety margins to account for disturbances and uncertainties
- **Dynamic Balance**: Ability to maintain balance during motion

```python
class BalanceChecker:
    def __init__(self):
        self.balance_threshold = 0.1  # meters from support polygon edge
        self.com_height = 0.85        # approximate CoM height for humanoid

    def is_balance_maintained(self, left_foot, right_foot, com_position):
        """Check if CoM position maintains balance"""
        # Calculate support polygon from foot positions
        support_polygon = self.calculate_support_polygon(left_foot, right_foot)

        # Project CoM to ground plane
        com_ground = (com_position.x, com_position.y)

        # Check if CoM is within support polygon with safety margin
        is_stable = self.is_point_in_polygon_with_margin(
            com_ground[0], com_ground[1],
            support_polygon, self.balance_threshold
        )

        return is_stable

    def calculate_support_polygon(self, left_foot, right_foot):
        """Calculate support polygon based on foot positions"""
        # Create polygon encompassing both feet
        min_x = min(left_foot.x, right_foot.x) - 0.1  # Add foot size margin
        max_x = max(left_foot.x, right_foot.x) + 0.1
        min_y = min(left_foot.y, right_foot.y) - 0.1
        max_y = max(left_foot.y, right_foot.y) + 0.1

        return [(min_x, min_y), (min_x, max_y), (max_x, max_y), (max_x, min_y)]

    def is_point_in_polygon_with_margin(self, x, y, polygon, margin):
        """Check if point is inside polygon with margin"""
        # First check if point is inside original polygon
        if not self.is_point_in_polygon(x, y, polygon):
            return False

        # Then check distance to edges to ensure margin
        min_distance = float('inf')
        for i in range(len(polygon)):
            p1 = polygon[i]
            p2 = polygon[(i + 1) % len(polygon)]
            distance = self.point_to_line_distance(x, y, p1, p2)
            min_distance = min(min_distance, distance)

        return min_distance >= margin

    def is_point_in_polygon(self, x, y, polygon):
        """Ray casting algorithm to check if point is in polygon"""
        n = len(polygon)
        inside = False

        p1x, p1y = polygon[0]
        for i in range(1, n + 1):
            p2x, p2y = polygon[i % n]
            if y > min(p1y, p2y):
                if y <= max(p1y, p2y):
                    if x <= max(p1x, p2x):
                        if p1y != p2y:
                            xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                        if p1x == p2x or x <= xinters:
                            inside = not inside
            p1x, p1y = p2x, p2y

        return inside

    def point_to_line_distance(self, px, py, p1, p2):
        """Calculate distance from point to line segment"""
        x1, y1 = p1
        x2, y2 = p2

        # Vector from p1 to p2
        dx = x2 - x1
        dy = y2 - y1

        # Length squared of line segment
        length_sq = dx*dx + dy*dy

        if length_sq == 0:
            # Points are the same, return distance to point
            return ((px - x1)**2 + (py - y1)**2)**0.5

        # Calculate projection of point onto line
        t = max(0, min(1, ((px - x1) * dx + (py - y1) * dy) / length_sq))

        # Calculate closest point on line segment
        closest_x = x1 + t * dx
        closest_y = y1 + t * dy

        # Return distance to closest point
        return ((px - closest_x)**2 + (py - closest_y)**2)**0.5
```

#### 3. Dynamic Constraints
Humanoid robots must consider dynamic effects during navigation:

- **Inertia**: The robot's resistance to changes in motion
- **Angular Momentum**: Conservation of angular momentum during movement
- **Ground Contact**: Maintaining proper contact with the ground during steps
- **Impact Forces**: Managing forces during foot contact with ground

### Navigation-Specific Constraints

#### 1. Obstacle Clearance
Humanoid robots require different obstacle clearance considerations:

- **Step-Over Capability**: Ability to step over obstacles up to maximum step height
- **Stair Navigation**: Ability to navigate stairs and level changes
- **Narrow Passages**: Minimum passage width considering robot body dimensions
- **Surface Traversability**: Ability to walk on different surface types

#### 2. Turning and Maneuvering
Bipedal turning has unique characteristics:

- **Pivot Turning**: Turning in place by pivoting around one foot
- **Step Turning**: Turning by taking multiple small steps
- **Strategic Turning**: Planning turns to maintain balance and stability
- **Gait Adaptation**: Adapting gait patterns for turning motions

```python
class HumanoidPathConstraints:
    def __init__(self):
        self.constraints = BipedalConstraints()
        self.balance_checker = BalanceChecker()

    def adjust_path_for_bipedal_constraints(self, original_path):
        """Adjust a planned path to respect humanoid constraints"""
        adjusted_path = []

        for i, pose in enumerate(original_path.poses):
            if i == 0:
                # Add first pose directly
                adjusted_path.append(pose)
            else:
                prev_pose = adjusted_path[-1]

                # Check if direct step is feasible
                feasible, reason = self.constraints.is_step_feasible(
                    prev_pose.pose.position, pose.pose.position
                )

                if feasible:
                    # Check if step maintains balance
                    if self.check_balance_along_path(prev_pose, pose):
                        adjusted_path.append(pose)
                    else:
                        # Interpolate to maintain balance
                        interpolated = self.interpolate_for_balance(prev_pose, pose)
                        adjusted_path.extend(interpolated)
                else:
                    # Interpolate to respect constraints
                    interpolated = self.interpolate_for_constraints(prev_pose, pose, reason)
                    adjusted_path.extend(interpolated)

        return adjusted_path

    def check_balance_along_path(self, start_pose, end_pose):
        """Check if path maintains balance between poses"""
        # For simplicity, just check if end pose maintains balance
        # In practice, this would check multiple intermediate points
        return True  # Placeholder - implement based on robot model

    def interpolate_for_balance(self, start_pose, end_pose):
        """Create intermediate waypoints to maintain balance"""
        intermediate_poses = []

        # Calculate intermediate points
        steps_needed = self.calculate_interpolation_steps(start_pose, end_pose)

        for i in range(1, steps_needed + 1):
            ratio = i / (steps_needed + 1)
            intermediate_pose = self.interpolate_pose(start_pose, end_pose, ratio)
            intermediate_poses.append(intermediate_pose)

        return intermediate_poses

    def interpolate_for_constraints(self, start_pose, end_pose, constraint_violation):
        """Create intermediate waypoints to respect constraints"""
        intermediate_poses = []

        # Calculate how many intermediate steps are needed
        distance = self.constraints.calculate_distance(
            start_pose.pose.position,
            end_pose.pose.position
        )

        # Determine number of steps based on max step length
        steps_needed = int(distance / self.constraints.max_step_length) + 1

        for i in range(1, steps_needed + 1):
            ratio = i / (steps_needed + 1)
            intermediate_pose = self.interpolate_pose(start_pose, end_pose, ratio)
            intermediate_poses.append(intermediate_pose)

        return intermediate_poses

    def interpolate_pose(self, start_pose, end_pose, ratio):
        """Interpolate between two poses"""
        from geometry_msgs.msg import PoseStamped
        import math

        intermediate = PoseStamped()
        intermediate.header = end_pose.header

        # Interpolate position
        intermediate.pose.position.x = start_pose.pose.position.x + \
            ratio * (end_pose.pose.position.x - start_pose.pose.position.x)
        intermediate.pose.position.y = start_pose.pose.position.y + \
            ratio * (end_pose.pose.position.y - start_pose.pose.position.y)
        intermediate.pose.position.z = start_pose.pose.position.z + \
            ratio * (end_pose.pose.position.z - start_pose.pose.position.z)

        # Interpolate orientation (simplified - in practice use quaternion interpolation)
        intermediate.pose.orientation = end_pose.pose.orientation

        return intermediate

    def calculate_interpolation_steps(self, start_pose, end_pose):
        """Calculate number of intermediate steps needed"""
        distance = self.constraints.calculate_distance(
            start_pose.pose.position,
            end_pose.pose.position
        )
        return int(distance / (self.constraints.max_step_length * 0.8))  # 80% of max for safety
```

### Implementing Bipedal-Aware Navigation

#### 1. Custom Costmap Layers
For humanoid robots, custom costmap layers are needed to account for bipedal constraints:

```yaml
# humanoid_costmap_params.yaml
local_costmap:
  plugins:
    - {name: static_layer, type: "nav2_costmap_2d::StaticLayer"}
    - {name: obstacle_layer, type: "nav2_costmap_2d::ObstacleLayer"}
    - {name: inflation_layer, type: "nav2_costmap_2d::InflationLayer"}
    - {name: step_height_layer, type: "humanoid_navigation::StepHeightLayer"}
    - {name: balance_layer, type: "humanoid_navigation::BalanceLayer"}

global_costmap:
  plugins:
    - {name: static_layer, type: "nav2_costmap_2d::StaticLayer"}
    - {name: obstacle_layer, type: "nav2_costmap_2d::ObstacleLayer"}
    - {name: inflation_layer, type: "nav2_costmap_2d::InflationLayer"}
    - {name: step_height_layer, type: "humanoid_navigation::StepHeightLayer"}
    - {name: balance_layer, type: "humanoid_navigation::BalanceLayer"}
```

#### 2. Footstep Planner Integration
Integrating footstep planning with Nav2:

```python
class FootstepPlanner:
    def __init__(self):
        self.foot_size = (0.25, 0.15)  # Length x Width in meters
        self.max_step_length = 0.60
        self.max_step_width = 0.40
        self.min_step_width = 0.20

    def plan_footsteps(self, path, start_foot_pose, is_left_foot_first=True):
        """Plan footstep sequence from a path"""
        footsteps = []

        current_foot_pose = start_foot_pose
        current_is_left = is_left_foot_first

        for i, path_pose in enumerate(path.poses):
            # Calculate required step to reach path pose
            step_required = self.calculate_required_step(current_foot_pose, path_pose.pose)

            if self.is_step_feasible(step_required):
                # Add footstep to sequence
                footstep = self.create_footstep(current_foot_pose, path_pose.pose, current_is_left)
                footsteps.append(footstep)

                # Update for next step
                current_foot_pose = path_pose.pose
                current_is_left = not current_is_left
            else:
                # Need to add intermediate steps
                intermediate_steps = self.generate_intermediate_steps(
                    current_foot_pose, path_pose.pose
                )
                for step in intermediate_steps:
                    footstep = self.create_footstep(current_foot_pose, step, current_is_left)
                    footsteps.append(footstep)
                    current_foot_pose = step
                    current_is_left = not current_is_left

        return footsteps

    def calculate_required_step(self, from_pose, to_pose):
        """Calculate the step required from one pose to another"""
        dx = to_pose.position.x - from_pose.position.x
        dy = to_pose.position.y - from_pose.position.y
        dz = to_pose.position.z - from_pose.position.z

        step_length = (dx*dx + dy*dy)**0.5

        return {
            'length': step_length,
            'height': abs(dz),
            'direction': (dx, dy)
        }

    def is_step_feasible(self, step):
        """Check if a step is feasible for humanoid robot"""
        if step['length'] > self.max_step_length:
            return False
        if step['height'] > 0.15:  # Maximum step height
            return False
        return True

    def create_footstep(self, position, orientation, is_left_foot):
        """Create a footstep at the given position"""
        from geometry_msgs.msg import Pose
        footstep = Pose()
        footstep.position = position
        footstep.orientation = orientation
        footstep.header = {"is_left_foot": is_left_foot}
        return footstep
```

## Trajectory Planning Algorithms for Humanoid Locomotion

Trajectory planning for humanoid robots requires specialized algorithms that account for the unique dynamics and constraints of bipedal locomotion. Unlike wheeled robots, humanoid robots must plan both the overall path and the detailed footstep sequence to maintain balance and stability.

### Classical Trajectory Planning Approaches

#### 1. Footstep Planning Algorithms

Footstep planning is a critical component of humanoid navigation that determines where and when each foot should be placed to achieve stable locomotion.

##### A* Footstep Planner
The A* algorithm can be adapted for footstep planning by treating each potential footstep location as a node in a graph:

```python
import heapq
import math
from collections import defaultdict

class AStarFootstepPlanner:
    def __init__(self, step_size=0.3, turn_angle=math.pi/6):
        self.step_size = step_size  # Distance between adjacent footsteps
        self.turn_angle = turn_angle  # Turning resolution
        self.max_step_height = 0.15  # Maximum step height
        self.max_step_width = 0.40   # Maximum lateral step

    def plan_footsteps(self, start_pose, goal_pose, costmap):
        """Plan sequence of footsteps using A* algorithm"""
        # Define possible step patterns (relative to current pose)
        step_patterns = self.generate_step_patterns()

        # Priority queue: (cost, pose, path)
        open_set = [(0, start_pose, [start_pose])]
        closed_set = set()

        # Cost tracking
        g_score = {self.pose_to_key(start_pose): 0}

        while open_set:
            current_cost, current_pose, current_path = heapq.heappop(open_set)

            # Check if we've reached the goal
            if self.is_at_goal(current_pose, goal_pose):
                return current_path

            pose_key = self.pose_to_key(current_pose)
            if pose_key in closed_set:
                continue

            closed_set.add(pose_key)

            # Generate possible next footsteps
            for step in step_patterns:
                next_pose = self.apply_step(current_pose, step)

                # Check feasibility
                if not self.is_step_feasible(current_pose, next_pose, costmap):
                    continue

                tentative_g_score = g_score[pose_key] + self.calculate_step_cost(current_pose, next_pose)

                next_pose_key = self.pose_to_key(next_pose)
                if next_pose_key in closed_set and tentative_g_score >= g_score.get(next_pose_key, float('inf')):
                    continue

                if tentative_g_score < g_score.get(next_pose_key, float('inf')):
                    g_score[next_pose_key] = tentative_g_score
                    h_score = self.heuristic(next_pose, goal_pose)
                    f_score = tentative_g_score + h_score

                    new_path = current_path + [next_pose]
                    heapq.heappush(open_set, (f_score, next_pose, new_path))

        return None  # No path found

    def generate_step_patterns(self):
        """Generate possible step patterns relative to current pose"""
        patterns = []

        # Forward steps
        for i in range(1, 4):  # 3 forward step options
            step_length = i * self.step_size
            patterns.append({
                'dx': step_length,
                'dy': 0,
                'dtheta': 0,
                'type': 'forward'
            })

        # Lateral steps
        for i in [-1, 1]:  # Left and right
            patterns.append({
                'dx': 0,
                'dy': i * self.step_size,
                'dtheta': 0,
                'type': 'lateral'
            })

        # Diagonal steps
        for dx_mult in [-1, 0, 1]:
            for dy_mult in [-1, 1]:
                if dx_mult == 0 and abs(dy_mult) == 1:  # Already covered by lateral
                    continue
                if dx_mult != 0:
                    patterns.append({
                        'dx': dx_mult * self.step_size,
                        'dy': dy_mult * self.step_size * 0.5,
                        'dtheta': 0,
                        'type': 'diagonal'
                    })

        # Turning steps
        for turn_dir in [-1, 1]:  # Left and right turns
            patterns.append({
                'dx': self.step_size * 0.5,
                'dy': turn_dir * self.step_size * 0.3,
                'dtheta': turn_dir * self.turn_angle,
                'type': 'turning'
            })

        return patterns

    def apply_step(self, current_pose, step_pattern):
        """Apply a step pattern to current pose to get next pose"""
        from geometry_msgs.msg import Pose
        import math

        next_pose = Pose()

        # Calculate new position based on current orientation
        cos_theta = math.cos(current_pose.orientation.z)  # Simplified orientation
        sin_theta = math.sin(current_pose.orientation.z)

        local_dx = step_pattern['dx']
        local_dy = step_pattern['dy']

        # Transform local step to global frame
        global_dx = local_dx * cos_theta - local_dy * sin_theta
        global_dy = local_dx * sin_theta + local_dy * cos_theta

        next_pose.position.x = current_pose.position.x + global_dx
        next_pose.position.y = current_pose.position.y + global_dy
        next_pose.position.z = current_pose.position.z  # For now, assume flat terrain

        # Update orientation
        next_pose.orientation.z = current_pose.orientation.z + step_pattern['dtheta']

        return next_pose

    def is_step_feasible(self, from_pose, to_pose, costmap):
        """Check if a step is feasible"""
        # Check step length
        dx = to_pose.position.x - from_pose.position.x
        dy = to_pose.position.y - from_pose.position.y
        step_length = math.sqrt(dx*dx + dy*dy)

        if step_length > self.max_step_width * 2:  # Rough check
            return False

        # Check for obstacles in step path
        if self.has_obstacles_in_path(from_pose, to_pose, costmap):
            return False

        return True

    def has_obstacles_in_path(self, from_pose, to_pose, costmap):
        """Check if path between poses has obstacles"""
        # Simplified implementation - in practice would check costmap values along path
        return False

    def calculate_step_cost(self, from_pose, to_pose):
        """Calculate cost of taking a step"""
        dx = to_pose.position.x - from_pose.position.x
        dy = to_pose.position.y - from_pose.position.y
        return math.sqrt(dx*dx + dy*dy)  # Euclidean distance cost

    def heuristic(self, pose1, pose2):
        """Heuristic function for A* (Euclidean distance)"""
        dx = pose2.position.x - pose1.position.x
        dy = pose2.position.y - pose1.position.y
        return math.sqrt(dx*dx + dy*dy)

    def is_at_goal(self, current_pose, goal_pose, tolerance=0.3):
        """Check if current pose is close enough to goal"""
        dx = goal_pose.position.x - current_pose.position.x
        dy = goal_pose.position.y - current_pose.position.y
        distance = math.sqrt(dx*dx + dy*dy)
        return distance <= tolerance

    def pose_to_key(self, pose):
        """Convert pose to hashable key"""
        # Discretize pose for use as dictionary key
        x_disc = round(pose.position.x / 0.1)  # 10cm resolution
        y_disc = round(pose.position.y / 0.1)
        theta_disc = round(pose.orientation.z / (math.pi/12))  # 15 degree resolution
        return (x_disc, y_disc, theta_disc)
```

##### Pattern-Based Footstep Planning
Pattern-based planning uses predefined gait patterns for more natural humanoid locomotion:

```python
class PatternBasedFootstepPlanner:
    def __init__(self):
        self.gait_patterns = {
            'walk': self.create_walk_pattern(),
            'turn_left': self.create_turn_pattern(-1),
            'turn_right': self.create_turn_pattern(1),
            'step_over': self.create_step_over_pattern(),
            'climb': self.create_climb_pattern()
        }

    def create_walk_pattern(self):
        """Create a basic walking gait pattern"""
        # Alternating left-right steps with appropriate spacing
        pattern = []

        # Left foot step
        pattern.append({
            'offset': (0.3, 0.15, 0),  # Forward and slight outward
            'timing': 0.0,
            'support': 'right'
        })

        # Right foot step
        pattern.append({
            'offset': (0.3, -0.15, 0),  # Forward and slight inward
            'timing': 0.5,  # Half cycle later
            'support': 'left'
        })

        return pattern

    def create_turn_pattern(self, direction):
        """Create turning gait pattern (direction: -1 for left, 1 for right)"""
        pattern = []

        # Turning involves different foot placement
        pattern.append({
            'offset': (0.15, direction * 0.2, 0),
            'timing': 0.0,
            'support': 'right' if direction > 0 else 'left'
        })

        pattern.append({
            'offset': (0.2, -direction * 0.1, direction * 0.1),
            'timing': 0.3,
            'support': 'left' if direction > 0 else 'right'
        })

        return pattern

    def plan_trajectory(self, path, robot_state):
        """Plan trajectory using gait patterns"""
        trajectory = []

        for i, path_pose in enumerate(path.poses):
            if i == 0:
                continue  # Skip first pose, use as starting point

            prev_pose = path.poses[i-1]

            # Determine required motion type
            motion_type = self.determine_motion_type(prev_pose, path_pose)

            # Get appropriate gait pattern
            pattern = self.gait_patterns.get(motion_type, self.gait_patterns['walk'])

            # Apply pattern to generate footstep sequence
            footsteps = self.apply_gait_pattern(
                prev_pose, path_pose, pattern, robot_state
            )

            trajectory.extend(footsteps)

        return trajectory

    def determine_motion_type(self, from_pose, to_pose):
        """Determine what type of motion is needed"""
        dx = to_pose.position.x - from_pose.position.x
        dy = to_pose.position.y - from_pose.position.y
        distance = math.sqrt(dx*dx + dy*dy)

        # Calculate heading change
        target_angle = math.atan2(dy, dx)
        current_angle = self.get_pose_yaw(from_pose)
        angle_diff = target_angle - current_angle

        # Normalize angle difference
        while angle_diff > math.pi:
            angle_diff -= 2 * math.pi
        while angle_diff < -math.pi:
            angle_diff += 2 * math.pi

        # Determine motion type based on distance and angle change
        if abs(angle_diff) > math.pi / 4:  # Significant turn
            return 'turn_left' if angle_diff < 0 else 'turn_right'
        elif distance > 0.5:  # Forward motion
            return 'walk'
        else:  # Small adjustment
            return 'adjust'

    def get_pose_yaw(self, pose):
        """Extract yaw angle from pose orientation"""
        # Simplified - in practice would use proper quaternion to euler conversion
        return pose.orientation.z
```

#### 2. Center of Mass Trajectory Planning

Maintaining the center of mass (CoM) within the support polygon is crucial for humanoid stability:

```python
class CoMTrajectoryPlanner:
    def __init__(self):
        self.com_height = 0.85  # Typical humanoid CoM height
        self.support_margin = 0.05  # Safety margin for support polygon

    def plan_com_trajectory(self, footstep_sequence, timing):
        """Plan CoM trajectory that maintains balance throughout footstep sequence"""
        com_trajectory = []

        for i, footstep in enumerate(footstep_sequence):
            # Calculate support polygon based on current and next foot positions
            support_polygon = self.calculate_support_polygon(
                footstep_sequence, i
            )

            # Plan CoM position within support polygon
            com_pos = self.plan_com_position(
                support_polygon, footstep, i, len(footstep_sequence)
            )

            # Add timing information
            com_pos_with_timing = {
                'position': com_pos,
                'time': timing[i] if i < len(timing) else i * 0.5
            }

            com_trajectory.append(com_pos_with_timing)

        return com_trajectory

    def calculate_support_polygon(self, footsteps, current_step_idx):
        """Calculate support polygon based on foot positions"""
        # For single support (one foot down)
        if current_step_idx < len(footsteps) - 1:
            # Currently in single support phase
            support_foot = footsteps[current_step_idx]['position']
            return self.create_single_support_polygon(support_foot)
        else:
            # In double support phase (both feet down) - if applicable
            if current_step_idx > 0:
                left_foot = footsteps[current_step_idx-1]['position']
                right_foot = footsteps[current_step_idx]['position']
                return self.create_double_support_polygon(left_foot, right_foot)
            else:
                # Single foot, use that foot's area
                return self.create_single_support_polygon(footsteps[current_step_idx]['position'])

    def create_single_support_polygon(self, foot_pos):
        """Create support polygon for single foot support"""
        # Simplified - in reality would use actual foot dimensions
        margin = 0.05
        return [
            (foot_pos.x - 0.1 - margin, foot_pos.y - 0.05 - margin),
            (foot_pos.x - 0.1 - margin, foot_pos.y + 0.05 + margin),
            (foot_pos.x + 0.1 + margin, foot_pos.y + 0.05 + margin),
            (foot_pos.x + 0.1 + margin, foot_pos.y - 0.05 - margin)
        ]

    def create_double_support_polygon(self, left_foot, right_foot):
        """Create support polygon for double foot support"""
        # Convex hull of both feet
        return [
            (min(left_foot.x, right_foot.x) - 0.1, min(left_foot.y, right_foot.y) - 0.05),
            (min(left_foot.x, right_foot.x) - 0.1, max(left_foot.y, right_foot.y) + 0.05),
            (max(left_foot.x, right_foot.x) + 0.1, max(left_foot.y, right_foot.y) + 0.05),
            (max(left_foot.x, right_foot.x) + 0.1, min(left_foot.y, right_foot.y) - 0.05)
        ]

    def plan_com_position(self, support_polygon, target_footstep, step_idx, total_steps):
        """Plan CoM position within support polygon"""
        import random

        # Simple approach: keep CoM near center of support polygon
        # with gradual transition toward next support polygon
        center_x = sum(p[0] for p in support_polygon) / len(support_polygon)
        center_y = sum(p[1] for p in support_polygon) / len(support_polygon)

        # Add some anticipation toward next step
        if step_idx < total_steps - 1:
            # Move CoM slightly toward where next foot will be placed
            next_step = target_footstep  # This would be the next footstep
            anticipation_x = 0.7 * (next_step['position'].x - center_x)
            anticipation_y = 0.7 * (next_step['position'].y - center_y)

            center_x = center_x * 0.3 + anticipation_x * 0.7
            center_y = center_y * 0.3 + anticipation_y * 0.7

        return (center_x, center_y, self.com_height)
```

### Advanced Trajectory Planning Techniques

#### 1. Model Predictive Control (MPC) for Humanoid Navigation

MPC is particularly effective for humanoid navigation as it can handle the dynamic constraints in real-time:

```python
class HumanoidMPCController:
    def __init__(self, prediction_horizon=10, dt=0.1):
        self.prediction_horizon = prediction_horizon
        self.dt = dt
        self.com_height = 0.85
        self.gravity = 9.81

    def solve_mpc_problem(self, current_state, reference_trajectory):
        """Solve MPC optimization problem for humanoid navigation"""
        # Simplified MPC implementation
        # In practice, this would use a proper optimization solver

        # Linear inverted pendulum model for CoM dynamics
        # CoM dynamics: d²x/dt² = g/h * (x - px) where (px,py) is ZMP position

        optimal_controls = []

        # Predict future states and optimize
        for k in range(self.prediction_horizon):
            # Get reference state for this time step
            ref_state = self.get_reference_state(reference_trajectory, k * self.dt)

            # Calculate control to track reference (simplified)
            control = self.calculate_control_to_track_reference(
                current_state, ref_state
            )

            optimal_controls.append(control)

            # Update current state with control
            current_state = self.predict_next_state(current_state, control)

        # Return first control (receding horizon)
        return optimal_controls[0] if optimal_controls else None

    def calculate_control_to_track_reference(self, current_state, reference_state):
        """Calculate control to track reference state"""
        # Simple proportional control with preview
        kp_pos = 2.0  # Position gain
        kp_vel = 1.5  # Velocity gain

        pos_error = (
            reference_state['com_pos'][0] - current_state['com_pos'][0],
            reference_state['com_pos'][1] - current_state['com_pos'][1]
        )

        vel_error = (
            reference_state['com_vel'][0] - current_state['com_vel'][0],
            reference_state['com_vel'][1] - current_state['com_vel'][1]
        )

        control = (
            kp_pos * pos_error[0] + kp_vel * vel_error[0],
            kp_pos * pos_error[1] + kp_vel * vel_error[1]
        )

        return control

    def predict_next_state(self, current_state, control):
        """Predict next state based on current state and control"""
        # Simplified dynamics integration
        new_state = current_state.copy()

        # Update CoM position based on velocity
        new_state['com_pos'] = (
            current_state['com_pos'][0] + current_state['com_vel'][0] * self.dt,
            current_state['com_pos'][1] + current_state['com_vel'][1] * self.dt,
            current_state['com_pos'][2]  # Height remains constant
        )

        # Update velocity based on control input (simplified)
        new_state['com_vel'] = (
            current_state['com_vel'][0] + control[0] * self.dt,
            current_state['com_vel'][1] + control[1] * self.dt,
            0  # Vertical velocity remains 0
        )

        return new_state

    def get_reference_state(self, trajectory, time):
        """Get reference state from trajectory at given time"""
        # Interpolate trajectory at specified time
        if not trajectory:
            return {'com_pos': (0, 0, self.com_height), 'com_vel': (0, 0, 0)}

        # Simplified - return first reference point
        return trajectory[0]
```

#### 2. Dynamic Movement Primitives (DMP) for Humanoid Locomotion

DMPs can be used to generate adaptive locomotion patterns:

```python
class HumanoidDMPController:
    def __init__(self, num_basis_functions=10):
        self.num_basis_functions = num_basis_functions
        self.basis_functions = self.initialize_basis_functions()
        self.weights = None  # Will be learned for different gaits

    def initialize_basis_functions(self):
        """Initialize basis functions for DMP"""
        import numpy as np

        basis_functions = []

        # Create Gaussian basis functions spread over the canonical system
        for i in range(self.num_basis_functions):
            center = i / (self.num_basis_functions - 1)  # From 0 to 1
            width = 1.0 / (self.num_basis_functions * 0.3)  # Overlap between functions

            basis_functions.append({
                'center': center,
                'width': width,
                'activation': lambda x, c=center, w=width: np.exp(-w * (x - c)**2)
            })

        return basis_functions

    def canonical_system(self, t, t_final):
        """Canonical system that decreases from 1 to 0"""
        if t_final <= 0:
            return 0
        return max(0, 1 - t / t_final)

    def learn_gait_pattern(self, demonstration_trajectory):
        """Learn a gait pattern from demonstration"""
        import numpy as np

        # Extract position and velocity from demonstration
        positions = np.array([[p['x'], p['y']] for p in demonstration_trajectory])
        velocities = self.compute_velocities(positions)
        accelerations = self.compute_accelerations(positions)

        # Compute forcing term for the DMP
        # s = canonical system value (decreases from 1 to 0)
        # y = position, dy = velocity, ddy = acceleration
        # ddy = α(β(g-y) - dy) + f(s)  =>  f(s) = ddy - α(β(g-y) - dy)

        alpha = 25.0  # DMP parameter
        beta = alpha / 4.0  # DMP parameter

        # Goal position
        goal = positions[-1]
        start = positions[0]

        # Compute forcing terms for each time step
        forcing_terms = []
        canonical_values = []

        for i, (pos, vel, acc) in enumerate(zip(positions, velocities, accelerations)):
            t = i * 0.01  # Assuming 100Hz control rate
            s = self.canonical_system(t, len(positions) * 0.01)

            # Desired acceleration from demonstration
            desired_acc = acc

            # Acceleration from spring-damper system
            spring_damper_acc = alpha * (beta * (goal - pos) - vel)

            # Forcing term
            forcing = desired_acc - spring_damper_acc

            forcing_terms.append(forcing)
            canonical_values.append(s)

        # Learn weights by fitting basis functions to forcing terms
        weights = self.fit_weights(canonical_values, forcing_terms)
        self.weights = weights

        return weights

    def fit_weights(self, canonical_values, forcing_terms):
        """Fit weights to approximate the forcing terms"""
        import numpy as np

        # For each basis function, compute activations
        activations = np.zeros((len(canonical_values), self.num_basis_functions))

        for i, s in enumerate(canonical_values):
            for j, bf in enumerate(self.basis_functions):
                activations[i, j] = bf['activation'](s)

        # Solve for weights: A * w = f
        # Using least squares solution
        weights = np.linalg.lstsq(activations, np.array(forcing_terms), rcond=None)[0]

        return weights

    def execute_gait(self, start_pos, goal_pos, duration):
        """Execute learned gait pattern"""
        import numpy as np

        if self.weights is None:
            raise ValueError("No gait pattern learned. Call learn_gait_pattern first.")

        # Initialize DMP state
        y = np.array(start_pos[:2])  # x, y position
        dy = np.array([0.0, 0.0])    # Initial velocity

        # DMP parameters
        alpha = 25.0
        beta = alpha / 4.0
        dt = 0.01  # 100Hz control rate

        trajectory = []

        for t in np.arange(0, duration, dt):
            # Canonical system
            s = self.canonical_system(t, duration)

            # Compute forcing term from learned weights
            f = self.compute_forcing_term(s)

            # DMP dynamics
            ddy = alpha * (beta * (goal_pos[:2] - y) - dy) + f

            # Integrate
            dy += ddy * dt
            y += dy * dt

            trajectory.append({
                'position': (y[0], y[1], start_pos[2]),  # Keep z constant
                'velocity': (dy[0], dy[1], 0),
                'time': t
            })

        return trajectory

    def compute_forcing_term(self, s):
        """Compute forcing term at canonical system value s"""
        import numpy as np

        if self.weights is None:
            return np.array([0.0, 0.0])

        # Compute basis function activations
        activations = np.array([bf['activation'](s) for bf in self.basis_functions])

        # Weighted sum
        forcing = np.dot(activations, self.weights)

        return forcing

    def compute_velocities(self, positions):
        """Compute velocities from position sequence"""
        import numpy as np

        velocities = np.zeros_like(positions)

        for i in range(1, len(positions)):
            velocities[i] = (positions[i] - positions[i-1]) / 0.01  # Assuming 0.01s intervals

        # Forward difference for first point
        if len(positions) > 1:
            velocities[0] = velocities[1]

        return velocities

    def compute_accelerations(self, positions):
        """Compute accelerations from position sequence"""
        import numpy as np

        accelerations = np.zeros_like(positions)

        for i in range(1, len(positions) - 1):
            accelerations[i] = (positions[i+1] - 2*positions[i] + positions[i-1]) / (0.01**2)

        # Handle boundaries
        if len(positions) > 2:
            accelerations[0] = accelerations[1]
            accelerations[-1] = accelerations[-2]

        return accelerations
```

### Integration with Nav2

#### 1. Custom Global Planner for Humanoid Robots

```python
# In Python or C++, this would be implemented as a Nav2 plugin
class HumanoidGlobalPlanner:
    def __init__(self):
        self.footstep_planner = AStarFootstepPlanner()
        self.com_planner = CoMTrajectoryPlanner()
        self.constraints = HumanoidPathConstraints()

    def create_plan(self, start, goal, costmap_ros):
        """Create a plan from start to goal considering humanoid constraints"""
        # Get costmap data
        costmap = costmap_ros.get_costmap()

        # Plan footsteps using humanoid-aware algorithm
        footsteps = self.footstep_planner.plan_footsteps(
            start, goal, costmap
        )

        if footsteps is None:
            return None  # No valid path found

        # Verify path respects all humanoid constraints
        validated_path = self.constraints.adjust_path_for_bipedal_constraints(
            self.convert_to_path_format(footsteps)
        )

        if validated_path is None:
            return None  # Path violates constraints

        # Plan CoM trajectory to maintain balance
        timing = self.generate_footstep_timing(footsteps)
        com_trajectory = self.com_planner.plan_com_trajectory(footsteps, timing)

        # Combine footstep and CoM trajectories
        full_trajectory = self.combine_trajectories(validated_path, com_trajectory)

        return full_trajectory

    def convert_to_path_format(self, footsteps):
        """Convert footsteps to Nav2 path format"""
        from nav_msgs.msg import Path
        from geometry_msgs.msg import PoseStamped

        path = Path()

        for footstep in footsteps:
            pose_stamped = PoseStamped()
            pose_stamped.pose = footstep['pose']
            pose_stamped.header.frame_id = "map"
            path.poses.append(pose_stamped)

        return path

    def generate_footstep_timing(self, footsteps):
        """Generate timing information for footsteps"""
        timing = []
        current_time = 0.0

        for i in range(len(footsteps)):
            # Typical humanoid step timing (simplified)
            step_duration = 0.5  # seconds per step
            current_time += step_duration
            timing.append(current_time)

        return timing

    def combine_trajectories(self, path, com_trajectory):
        """Combine path and CoM trajectory into full navigation plan"""
        # This would create a comprehensive plan including both footstep
        # and CoM trajectory information
        return {
            'path': path,
            'com_trajectory': com_trajectory,
            'timing': self.generate_footstep_timing(path.poses)
        }
```

#### 2. Custom Local Planner for Humanoid Robots

```python
class HumanoidLocalPlanner:
    def __init__(self):
        self.mpc_controller = HumanoidMPCController()
        self.dmp_controller = HumanoidDMPController()
        self.balance_checker = BalanceChecker()

    def compute_velocity_commands(self, pose, velocity, goal, plan):
        """Compute velocity commands for local navigation"""
        # Get reference trajectory from global plan
        reference_trajectory = self.extract_reference_trajectory(
            plan, pose, look_ahead=5.0
        )

        # Use MPC to compute optimal commands
        optimal_control = self.mpc_controller.solve_mpc_problem(
            self.extract_robot_state(pose, velocity),
            reference_trajectory
        )

        # Convert control to velocity commands
        velocity_cmd = self.control_to_velocity(optimal_control, pose)

        # Verify balance constraints
        if not self.check_balance_feasibility(velocity_cmd, pose):
            # Use recovery behavior
            velocity_cmd = self.balance_recovery_velocity(pose)

        return velocity_cmd

    def extract_reference_trajectory(self, plan, current_pose, look_ahead):
        """Extract reference trajectory from global plan"""
        # Find closest point on plan to current pose
        closest_idx = self.find_closest_point(plan.poses, current_pose)

        # Extract future reference points
        reference_points = []
        distance = 0.0

        for i in range(closest_idx, len(plan.poses)):
            if i == closest_idx:
                continue

            prev_point = plan.poses[max(0, i-1)].pose.position
            curr_point = plan.poses[i].pose.position

            segment_length = self.distance_3d(
                prev_point, curr_point
            )

            if distance + segment_length > look_ahead:
                break

            reference_points.append({
                'position': (curr_point.x, curr_point.y, curr_point.z),
                'time': distance / 0.5  # Assuming 0.5 m/s average speed
            })

            distance += segment_length

        return reference_points

    def extract_robot_state(self, pose, velocity):
        """Extract robot state for controller"""
        return {
            'com_pos': (pose.position.x, pose.position.y, 0.85),  # Estimated CoM
            'com_vel': (velocity.linear.x, velocity.linear.y, 0.0)
        }

    def control_to_velocity(self, control, current_pose):
        """Convert control output to velocity command"""
        from geometry_msgs.msg import Twist

        cmd_vel = Twist()

        # Convert CoM control to base velocity
        cmd_vel.linear.x = control[0] * 0.5  # Scale appropriately
        cmd_vel.linear.y = control[1] * 0.5
        cmd_vel.angular.z = self.calculate_angular_velocity(
            control, current_pose
        )

        return cmd_vel

    def check_balance_feasibility(self, velocity_cmd, current_pose):
        """Check if velocity command maintains balance"""
        # Predict next CoM position based on velocity
        predicted_com = self.predict_com_position(
            current_pose, velocity_cmd
        )

        # Check if predicted position maintains balance
        return self.balance_checker.is_balance_maintained(
            self.get_left_foot_pose(current_pose),
            self.get_right_foot_pose(current_pose),
            predicted_com
        )

    def balance_recovery_velocity(self, current_pose):
        """Generate velocity command for balance recovery"""
        from geometry_msgs.msg import Twist

        # Simplified balance recovery - stop and adjust
        cmd_vel = Twist()
        cmd_vel.linear.x = 0.0
        cmd_vel.linear.y = 0.0
        cmd_vel.angular.z = 0.0

        return cmd_vel

    def distance_3d(self, p1, p2):
        """Calculate 3D distance between two points"""
        dx = p2.x - p1.x
        dy = p2.y - p1.y
        dz = p2.z - p1.z
        return (dx*dx + dy*dy + dz*dz)**0.5

    def find_closest_point(self, poses, target_pose):
        """Find index of closest point in poses to target pose"""
        min_distance = float('inf')
        closest_idx = 0

        for i, pose in enumerate(poses):
            distance = self.distance_3d(
                pose.pose.position,
                target_pose.position
            )

            if distance < min_distance:
                min_distance = distance
                closest_idx = i

        return closest_idx

    def predict_com_position(self, current_pose, velocity_cmd):
        """Predict CoM position based on velocity command"""
        dt = 0.1  # Prediction time step
        predicted_x = current_pose.position.x + velocity_cmd.linear.x * dt
        predicted_y = current_pose.position.y + velocity_cmd.linear.y * dt
        return (predicted_x, predicted_y, 0.85)  # Fixed height

    def get_left_foot_pose(self, robot_pose):
        """Get estimated left foot pose (simplified)"""
        # In practice, this would come from forward kinematics
        from geometry_msgs.msg import Point
        return Point(x=robot_pose.position.x - 0.1, y=robot_pose.position.y + 0.1, z=0.0)

    def get_right_foot_pose(self, robot_pose):
        """Get estimated right foot pose (simplified)"""
        # In practice, this would come from forward kinematics
        from geometry_msgs.msg import Point
        return Point(x=robot_pose.position.x + 0.1, y=robot_pose.position.y - 0.1, z=0.0)

    def calculate_angular_velocity(self, control, current_pose):
        """Calculate angular velocity from control and current pose"""
        # Simplified calculation
        return control[1] * 0.5  # Scale factor
```

## AI-Driven Control Systems for Navigation

Artificial Intelligence plays a crucial role in modern humanoid robot navigation, enabling adaptive, learning-based control systems that can handle complex and dynamic environments. AI-driven control systems can adapt to new situations, learn from experience, and make intelligent decisions in real-time.

### Machine Learning Approaches for Navigation

#### 1. Reinforcement Learning for Humanoid Navigation

Reinforcement Learning (RL) is particularly well-suited for humanoid navigation as it can learn complex behaviors through trial and error in simulation before deployment.

##### Deep Q-Network (DQN) for Footstep Planning

```python
import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
import random
from collections import deque

class DQN(nn.Module):
    def __init__(self, state_size, action_size):
        super(DQN, self).__init__()
        self.fc1 = nn.Linear(state_size, 128)
        self.fc2 = nn.Linear(128, 128)
        self.fc3 = nn.Linear(128, 64)
        self.fc4 = nn.Linear(64, action_size)

    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = torch.relu(self.fc2(x))
        x = torch.relu(self.fc3(x))
        return self.fc4(x)

class HumanoidNavigationDQN:
    def __init__(self, state_size=24, action_size=9):  # 9 possible footstep actions
        self.state_size = state_size
        self.action_size = action_size
        self.memory = deque(maxlen=10000)
        self.epsilon = 1.0  # Exploration rate
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.995
        self.learning_rate = 0.001
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        # Neural networks
        self.q_network = DQN(state_size, action_size).to(self.device)
        self.target_network = DQN(state_size, action_size).to(self.device)
        self.optimizer = optim.Adam(self.q_network.parameters(), lr=self.learning_rate)

        # Update target network
        self.update_target_network()

    def update_target_network(self):
        """Copy weights from main network to target network"""
        self.target_network.load_state_dict(self.q_network.state_dict())

    def remember(self, state, action, reward, next_state, done):
        """Store experience in replay memory"""
        self.memory.append((state, action, reward, next_state, done))

    def act(self, state):
        """Choose action using epsilon-greedy policy"""
        if np.random.random() <= self.epsilon:
            return random.randrange(self.action_size)

        state_tensor = torch.FloatTensor(state).unsqueeze(0).to(self.device)
        q_values = self.q_network(state_tensor)
        return np.argmax(q_values.cpu().data.numpy())

    def replay(self, batch_size=32):
        """Train the model on a batch of experiences"""
        if len(self.memory) < batch_size:
            return

        batch = random.sample(self.memory, batch_size)
        states = torch.FloatTensor([e[0] for e in batch]).to(self.device)
        actions = torch.LongTensor([e[1] for e in batch]).to(self.device)
        rewards = torch.FloatTensor([e[2] for e in batch]).to(self.device)
        next_states = torch.FloatTensor([e[3] for e in batch]).to(self.device)
        dones = torch.BoolTensor([e[4] for e in batch]).to(self.device)

        current_q_values = self.q_network(states).gather(1, actions.unsqueeze(1))
        next_q_values = self.target_network(next_states).max(1)[0].detach()
        target_q_values = rewards + (0.99 * next_q_values * ~dones)

        loss = nn.MSELoss()(current_q_values.squeeze(), target_q_values)

        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()

        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

    def train_step(self, state, action, reward, next_state, done):
        """Single training step"""
        self.remember(state, action, reward, next_state, done)
        self.replay()

        # Periodically update target network
        if len(self.memory) % 100 == 0:
            self.update_target_network()

class HumanoidNavigationEnvironment:
    def __init__(self):
        self.robot_state = {
            'left_foot': [0.0, 0.1, 0.0],
            'right_foot': [0.0, -0.1, 0.0],
            'com': [0.0, 0.0, 0.85],
            'goal': [5.0, 3.0, 0.0],
            'obstacles': [[2.0, 1.0, 0.2], [3.5, 2.5, 0.2]]  # x, y, radius
        }
        self.step_count = 0
        self.max_steps = 500

    def reset(self):
        """Reset environment to initial state"""
        self.robot_state = {
            'left_foot': [0.0, 0.1, 0.0],
            'right_foot': [0.0, -0.1, 0.0],
            'com': [0.0, 0.0, 0.85],
            'goal': [5.0, 3.0, 0.0],
            'obstacles': [[2.0, 1.0, 0.2], [3.5, 2.5, 0.2]]
        }
        self.step_count = 0
        return self.get_state()

    def get_state(self):
        """Get current state representation for RL"""
        state = []

        # Relative positions of feet to CoM
        state.extend([
            self.robot_state['left_foot'][0] - self.robot_state['com'][0],
            self.robot_state['left_foot'][1] - self.robot_state['com'][1],
            self.robot_state['right_foot'][0] - self.robot_state['com'][0],
            self.robot_state['right_foot'][1] - self.robot_state['com'][1]
        ])

        # Relative position to goal
        state.extend([
            self.robot_state['goal'][0] - self.robot_state['com'][0],
            self.robot_state['goal'][1] - self.robot_state['com'][1]
        ])

        # Nearest obstacles (up to 3)
        for i in range(3):
            if i < len(self.robot_state['obstacles']):
                obs = self.robot_state['obstacles'][i]
                state.extend([
                    obs[0] - self.robot_state['com'][0],
                    obs[1] - self.robot_state['com'][1]
                ])
            else:
                state.extend([10.0, 10.0])  # Far away if no obstacle

        # Current CoM velocity (assumed zero initially)
        state.extend([0.0, 0.0])

        return np.array(state)

    def step(self, action):
        """Execute action and return (next_state, reward, done, info)"""
        self.step_count += 1

        # Define possible footstep actions
        # 0-3: Move left foot in 4 directions
        # 4-7: Move right foot in 4 directions
        # 8: No step (for timing)
        step_offsets = [
            [0.3, 0.0, 0.0],    # Forward
            [-0.3, 0.0, 0.0],   # Backward
            [0.0, 0.2, 0.0],    # Left
            [0.0, -0.2, 0.0],   # Right
            [0.2, 0.1, 0.0],    # Forward-left
            [0.2, -0.1, 0.0],   # Forward-right
            [-0.2, 0.1, 0.0],   # Back-left
            [-0.2, -0.1, 0.0],  # Back-right
        ]

        if action < 8:
            # Execute footstep
            foot_to_move = 'left_foot' if self.step_count % 2 == 0 else 'right_foot'

            # Calculate new foot position
            offset = step_offsets[action]
            new_pos = [
                self.robot_state[foot_to_move][0] + offset[0],
                self.robot_state[foot_to_move][1] + offset[1],
                self.robot_state[foot_to_move][2] + offset[2]
            ]

            # Check if step is valid (not in obstacle, within bounds)
            if self.is_valid_step(new_pos):
                self.robot_state[foot_to_move] = new_pos
                # Update CoM based on new foot positions
                self.update_com_position()

        # Calculate reward
        reward = self.calculate_reward()

        # Check if episode is done
        done = self.is_done()

        next_state = self.get_state()

        return next_state, reward, done, {}

    def is_valid_step(self, new_pos):
        """Check if step is valid (not in obstacle, within bounds)"""
        # Check obstacle collision
        for obs in self.robot_state['obstacles']:
            dist = ((new_pos[0] - obs[0])**2 + (new_pos[1] - obs[1])**2)**0.5
            if dist < obs[2] + 0.1:  # 0.1m clearance
                return False

        # Check bounds (simple rectangular bounds)
        if abs(new_pos[0]) > 10 or abs(new_pos[1]) > 10:
            return False

        return True

    def update_com_position(self):
        """Update CoM position based on foot positions (simplified)"""
        # Simple averaging for demonstration
        left_pos = self.robot_state['left_foot']
        right_pos = self.robot_state['right_foot']

        # CoM is between feet, elevated
        self.robot_state['com'][0] = (left_pos[0] + right_pos[0]) / 2
        self.robot_state['com'][1] = (left_pos[1] + right_pos[1]) / 2
        # Height remains constant for now

    def calculate_reward(self):
        """Calculate reward based on current state"""
        # Distance to goal (negative, closer is better)
        dist_to_goal = ((self.robot_state['goal'][0] - self.robot_state['com'][0])**2 +
                       (self.robot_state['goal'][1] - self.robot_state['com'][1])**2)**0.5

        reward = -dist_to_goal * 0.1  # Negative distance penalty

        # Bonus for getting closer to goal
        if dist_to_goal < 0.5:
            reward += 10  # Reached goal

        # Penalty for invalid positions
        if not self.is_balance_maintained():
            reward -= 5  # Balance lost

        # Small time penalty to encourage efficiency
        reward -= 0.01

        return reward

    def is_balance_maintained(self):
        """Check if current foot positions maintain balance"""
        # Simplified balance check - CoM should be between feet
        left_x, left_y = self.robot_state['left_foot'][0], self.robot_state['left_foot'][1]
        right_x, right_y = self.robot_state['right_foot'][0], self.robot_state['right_foot'][1]
        com_x, com_y = self.robot_state['com'][0], self.robot_state['com'][1]

        # Create simple support polygon and check if CoM is inside
        min_x, max_x = min(left_x, right_x), max(left_x, right_x)
        min_y, max_y = min(left_y, right_y), max(left_y, right_y)

        # Add small margin for stability
        margin = 0.05
        return (min_x - margin <= com_x <= max_x + margin and
                min_y - margin <= com_y <= max_y + margin)

    def is_done(self):
        """Check if episode is done"""
        dist_to_goal = ((self.robot_state['goal'][0] - self.robot_state['com'][0])**2 +
                       (self.robot_state['goal'][1] - self.robot_state['com'][1])**2)**0.5

        return (dist_to_goal < 0.5 or  # Reached goal
                self.step_count >= self.max_steps or  # Max steps reached
                not self.is_balance_maintained())  # Balance lost
```

#### 2. Deep Learning for Terrain Classification and Navigation

Deep learning models can be used to classify terrain types and adjust navigation strategies accordingly:

```python
import torch
import torch.nn as nn
import torchvision.transforms as transforms
from PIL import Image

class TerrainClassificationNet(nn.Module):
    def __init__(self, num_classes=5):  # flat, rough, stairs, slope, obstacle
        super(TerrainClassificationNet, self).__init__()

        # Feature extraction backbone
        self.features = nn.Sequential(
            nn.Conv2d(3, 32, kernel_size=3, padding=1),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=2, stride=2),

            nn.Conv2d(32, 64, kernel_size=3, padding=1),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=2, stride=2),

            nn.Conv2d(64, 128, kernel_size=3, padding=1),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=2, stride=2),

            nn.Conv2d(128, 256, kernel_size=3, padding=1),
            nn.ReLU(inplace=True),
            nn.AdaptiveAvgPool2d((4, 4))
        )

        # Classifier
        self.classifier = nn.Sequential(
            nn.Dropout(),
            nn.Linear(256 * 4 * 4, 512),
            nn.ReLU(inplace=True),
            nn.Dropout(),
            nn.Linear(512, 128),
            nn.ReLU(inplace=True),
            nn.Linear(128, num_classes)
        )

    def forward(self, x):
        x = self.features(x)
        x = x.view(x.size(0), -1)
        x = self.classifier(x)
        return x

class TerrainAwareNavigation:
    def __init__(self):
        self.terrain_classifier = TerrainClassificationNet()
        self.load_pretrained_model()

        # Terrain-specific navigation parameters
        self.terrain_params = {
            0: {  # flat ground
                'max_velocity': 0.8,
                'step_size': 0.5,
                'foot_lift_height': 0.05,
                'stance_time': 0.4
            },
            1: {  # rough terrain
                'max_velocity': 0.3,
                'step_size': 0.2,
                'foot_lift_height': 0.1,
                'stance_time': 0.6
            },
            2: {  # stairs
                'max_velocity': 0.2,
                'step_size': 0.3,
                'foot_lift_height': 0.2,
                'stance_time': 0.8
            },
            3: {  # slope
                'max_velocity': 0.4,
                'step_size': 0.3,
                'foot_lift_height': 0.08,
                'stance_time': 0.5
            },
            4: {  # obstacle
                'max_velocity': 0.0,  # Stop
                'step_size': 0.0,
                'foot_lift_height': 0.15,
                'stance_time': 1.0
            }
        }

        # Image preprocessing
        self.transform = transforms.Compose([
            transforms.Resize((64, 64)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406],
                               std=[0.229, 0.224, 0.225])
        ])

    def load_pretrained_model(self):
        """Load a pre-trained terrain classification model"""
        # In practice, you would load a saved model state dict
        # self.terrain_classifier.load_state_dict(torch.load('terrain_model.pth'))
        pass

    def classify_terrain(self, image_path):
        """Classify terrain type from an image"""
        # Load and preprocess image
        image = Image.open(image_path).convert('RGB')
        input_tensor = self.transform(image).unsqueeze(0)

        # Run inference
        with torch.no_grad():
            outputs = self.terrain_classifier(input_tensor)
            _, predicted = torch.max(outputs, 1)

        terrain_type = predicted.item()
        confidence = torch.softmax(outputs, dim=1)[0][predicted].item()

        return terrain_type, confidence

    def get_navigation_params(self, terrain_type):
        """Get navigation parameters based on terrain type"""
        return self.terrain_params.get(terrain_type, self.terrain_params[0])

    def adjust_navigation_for_terrain(self, current_params, terrain_type):
        """Adjust navigation parameters based on terrain classification"""
        terrain_params = self.get_navigation_params(terrain_type)

        # Blend current parameters with terrain-specific parameters
        adjusted_params = {}
        for key in current_params:
            if key in terrain_params:
                # Use terrain-specific parameter
                adjusted_params[key] = terrain_params[key]
            else:
                # Keep original parameter
                adjusted_params[key] = current_params[key]

        return adjusted_params

    def process_camera_feed(self, camera_image):
        """Process camera feed for terrain classification"""
        # Save temporary image for processing
        import tempfile
        import os

        with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as tmp_file:
            camera_image.save(tmp_file.name)
            terrain_type, confidence = self.classify_terrain(tmp_file.name)
            os.unlink(tmp_file.name)

        return terrain_type, confidence
```

#### 3. Neural Network-Based Gait Generation

Neural networks can learn and generate natural gait patterns for different situations:

```python
import torch
import torch.nn as nn
import numpy as np

class GaitGenerationNet(nn.Module):
    def __init__(self, input_size=10, output_size=24):  # 24 joint angles for 2 steps
        super(GaitGenerationNet, self).__init__()

        self.network = nn.Sequential(
            nn.Linear(input_size, 64),
            nn.ReLU(),
            nn.Linear(64, 128),
            nn.ReLU(),
            nn.Linear(128, 128),
            nn.ReLU(),
            nn.Linear(128, 64),
            nn.ReLU(),
            nn.Linear(64, output_size),
            nn.Tanh()  # Output between -1 and 1
        )

    def forward(self, x):
        return self.network(x)

class NeuralGaitController:
    def __init__(self):
        self.gait_net = GaitGenerationNet()
        self.load_pretrained_gait_model()

        # Gait phase information
        self.phase_duration = 0.5  # seconds per phase
        self.current_phase = 0.0

    def load_pretrained_gait_model(self):
        """Load a pre-trained gait generation model"""
        # In practice, load a trained model
        pass

    def generate_gait_pattern(self, speed, direction, terrain_type, step_height=0.05):
        """Generate gait pattern based on inputs"""
        # Create input vector
        input_vector = torch.FloatTensor([
            speed,           # Desired speed (0-1)
            direction,       # Direction (-1 to 1 for turning)
            terrain_type,    # Terrain type
            step_height,     # Step height adjustment
            np.sin(self.current_phase),  # Phase information
            np.cos(self.current_phase),
            0.0, 0.0, 0.0, 0.0  # Additional context (e.g., balance, obstacles)
        ]).unsqueeze(0)

        # Generate gait pattern
        with torch.no_grad():
            gait_output = self.gait_net(input_vector)

        # Convert to joint angle commands
        joint_commands = self.convert_to_joint_angles(gait_output.squeeze().numpy())

        return joint_commands

    def convert_to_joint_angles(self, gait_output):
        """Convert network output to joint angle commands"""
        # Map network outputs to joint angles
        # This is a simplified mapping - in practice would be more complex
        joint_angles = {}

        # Hip joints (left and right)
        joint_angles['left_hip_roll'] = gait_output[0] * 0.3  # Limited range
        joint_angles['left_hip_pitch'] = gait_output[1] * 0.5
        joint_angles['left_hip_yaw'] = gait_output[2] * 0.2

        joint_angles['right_hip_roll'] = gait_output[3] * 0.3
        joint_angles['right_hip_pitch'] = gait_output[4] * 0.5
        joint_angles['right_hip_yaw'] = gait_output[5] * 0.2

        # Knee joints
        joint_angles['left_knee'] = gait_output[6] * 0.8
        joint_angles['right_knee'] = gait_output[7] * 0.8

        # Ankle joints
        joint_angles['left_ankle_pitch'] = gait_output[8] * 0.3
        joint_angles['left_ankle_roll'] = gait_output[9] * 0.2
        joint_angles['right_ankle_pitch'] = gait_output[10] * 0.3
        joint_angles['right_ankle_roll'] = gait_output[11] * 0.2

        # Arm joints for balance
        joint_angles['left_arm'] = gait_output[12] * 0.5
        joint_angles['right_arm'] = gait_output[13] * 0.5

        return joint_angles

    def update_phase(self, dt):
        """Update gait phase based on time step"""
        self.current_phase += 2 * np.pi * dt / self.phase_duration
        if self.current_phase >= 2 * np.pi:
            self.current_phase -= 2 * np.pi

class AIHumanoidController:
    def __init__(self):
        self.terrain_aware_nav = TerrainAwareNavigation()
        self.neural_gait_controller = NeuralGaitController()
        self.balance_checker = BalanceChecker()

        # Navigation state
        self.current_speed = 0.0
        self.current_direction = 0.0
        self.terrain_type = 0  # Default to flat ground
        self.last_terrain_check = 0.0

    def update_navigation(self, sensor_data, dt):
        """Update navigation based on sensor data"""
        # Check terrain periodically
        current_time = self.get_simulation_time()
        if current_time - self.last_terrain_check > 0.5:  # Check every 0.5 seconds
            terrain_type, confidence = self.terrain_aware_nav.process_camera_feed(
                sensor_data['camera_image']
            )
            if confidence > 0.7:  # Only update if confident
                self.terrain_type = terrain_type
                self.last_terrain_check = current_time

        # Get desired navigation command (from path planner or higher-level controller)
        desired_speed, desired_direction = self.get_desired_navigation_command()

        # Adjust speed based on terrain
        max_speed_for_terrain = self.terrain_aware_nav.get_navigation_params(
            self.terrain_type
        )['max_velocity']

        self.current_speed = min(desired_speed, max_speed_for_terrain)
        self.current_direction = desired_direction

        # Generate gait pattern
        gait_commands = self.neural_gait_controller.generate_gait_pattern(
            self.current_speed,
            self.current_direction,
            self.terrain_type
        )

        # Update gait phase
        self.neural_gait_controller.update_phase(dt)

        # Check balance
        balance_ok = self.balance_checker.is_balance_maintained(
            sensor_data['left_foot_pose'],
            sensor_data['right_foot_pose'],
            sensor_data['com_pose']
        )

        # If balance is compromised, adjust gait
        if not balance_ok:
            gait_commands = self.adjust_gait_for_balance(gait_commands)

        return gait_commands

    def get_desired_navigation_command(self):
        """Get desired navigation command from path planner"""
        # In practice, this would come from the path planner
        return 0.5, 0.0  # Default: half speed, straight ahead

    def get_simulation_time(self):
        """Get current simulation time"""
        import time
        return time.time()  # In practice, would use ROS time

    def adjust_gait_for_balance(self, original_gait_commands):
        """Adjust gait commands to improve balance"""
        # Simplified balance adjustment - increase ankle adjustments
        adjusted_commands = original_gait_commands.copy()

        # Increase ankle adjustments to improve balance
        for joint in ['left_ankle_pitch', 'left_ankle_roll', 'right_ankle_pitch', 'right_ankle_roll']:
            if joint in adjusted_commands:
                adjusted_commands[joint] *= 1.5  # Increase by 50%

        # Slow down movement
        self.current_speed *= 0.5

        return adjusted_commands
```

### Behavior Trees for Complex Navigation Tasks

Behavior trees provide a structured way to implement complex navigation behaviors:

```python
class BehaviorNode:
    def __init__(self, name):
        self.name = name
        self.status = "IDLE"  # IDLE, RUNNING, SUCCESS, FAILURE

    def tick(self):
        """Execute one cycle of the behavior"""
        pass

class SequenceNode(BehaviorNode):
    def __init__(self, name, children):
        super().__init__(name)
        self.children = children
        self.current_child_idx = 0

    def tick(self):
        """Execute children in sequence"""
        while self.current_child_idx < len(self.children):
            child = self.children[self.current_child_idx]
            child_status = child.tick()

            if child_status == "RUNNING":
                return "RUNNING"
            elif child_status == "FAILURE":
                self.current_child_idx = 0
                return "FAILURE"
            elif child_status == "SUCCESS":
                self.current_child_idx += 1

        # All children completed successfully
        self.current_child_idx = 0
        return "SUCCESS"

class SelectorNode(BehaviorNode):
    def __init__(self, name, children):
        super().__init__(name)
        self.children = children
        self.current_child_idx = 0

    def tick(self):
        """Execute children until one succeeds"""
        while self.current_child_idx < len(self.children):
            child = self.children[self.current_child_idx]
            child_status = child.tick()

            if child_status == "RUNNING":
                return "RUNNING"
            elif child_status == "SUCCESS":
                self.current_child_idx = 0
                return "SUCCESS"
            elif child_status == "FAILURE":
                self.current_child_idx += 1

        # All children failed
        self.current_child_idx = 0
        return "FAILURE"

class NavigateToGoalNode(BehaviorNode):
    def __init__(self, name, goal_pose):
        super().__init__(name)
        self.goal_pose = goal_pose
        self.path_planner = HumanoidGlobalPlanner()
        self.local_planner = HumanoidLocalPlanner()
        self.current_path = None
        self.path_idx = 0

    def tick(self):
        """Navigate to goal"""
        # Check if we have a path
        if self.current_path is None:
            # Plan path to goal
            self.current_path = self.path_planner.create_plan(
                self.get_current_pose(),
                self.goal_pose,
                self.get_costmap()
            )

            if self.current_path is None:
                return "FAILURE"

            self.path_idx = 0

        # Check if we reached the goal
        if self.has_reached_goal():
            self.current_path = None
            return "SUCCESS"

        # Follow the path
        velocity_cmd = self.local_planner.compute_velocity_commands(
            self.get_current_pose(),
            self.get_current_velocity(),
            self.goal_pose,
            self.current_path
        )

        # Send command to robot
        self.send_velocity_command(velocity_cmd)

        return "RUNNING"

    def get_current_pose(self):
        """Get current robot pose"""
        # In practice, this would come from localization
        pass

    def get_current_velocity(self):
        """Get current robot velocity"""
        # In practice, this would come from odometry
        pass

    def get_costmap(self):
        """Get current costmap"""
        # In practice, this would come from costmap server
        pass

    def has_reached_goal(self):
        """Check if robot has reached the goal"""
        current_pose = self.get_current_pose()
        goal_pose = self.goal_pose

        distance = ((current_pose.x - goal_pose.x)**2 +
                   (current_pose.y - goal_pose.y)**2)**0.5

        return distance < 0.3  # 30cm tolerance

    def send_velocity_command(self, cmd):
        """Send velocity command to robot"""
        # In practice, this would publish to cmd_vel topic
        pass

class AvoidObstaclesNode(BehaviorNode):
    def __init__(self, name):
        super().__init__(name)
        self.obstacle_detector = self.initialize_obstacle_detector()

    def initialize_obstacle_detector(self):
        """Initialize obstacle detection system"""
        # In practice, this would set up sensor processing
        return {}

    def tick(self):
        """Check for and avoid obstacles"""
        obstacles = self.detect_obstacles()

        if obstacles:
            # Implement obstacle avoidance
            avoidance_cmd = self.compute_avoidance_command(obstacles)
            self.send_velocity_command(avoidance_cmd)
            return "RUNNING"
        else:
            return "SUCCESS"  # No obstacles to avoid

    def detect_obstacles(self):
        """Detect obstacles using sensors"""
        # In practice, this would process sensor data
        return []

    def compute_avoidance_command(self, obstacles):
        """Compute velocity command to avoid obstacles"""
        # In practice, this would implement obstacle avoidance algorithm
        return None

    def send_velocity_command(self, cmd):
        """Send velocity command to robot"""
        pass

class MonitorBalanceNode(BehaviorNode):
    def __init__(self, name):
        super().__init__(name)
        self.balance_checker = BalanceChecker()
        self.recovery_active = False

    def tick(self):
        """Monitor robot balance"""
        current_pose = self.get_current_pose()
        left_foot = self.get_left_foot_pose()
        right_foot = self.get_right_foot_pose()

        is_balanced = self.balance_checker.is_balance_maintained(
            left_foot, right_foot, current_pose
        )

        if not is_balanced:
            if not self.recovery_active:
                # Start balance recovery
                self.start_balance_recovery()
                self.recovery_active = True
            return "RUNNING"  # Balance recovery is active
        else:
            if self.recovery_active:
                # Balance recovered
                self.stop_balance_recovery()
                self.recovery_active = False
            return "SUCCESS"

    def get_current_pose(self):
        """Get current robot pose"""
        pass

    def get_left_foot_pose(self):
        """Get left foot pose"""
        pass

    def get_right_foot_pose(self):
        """Get right foot pose"""
        pass

    def start_balance_recovery(self):
        """Start balance recovery procedure"""
        # In practice, this would send recovery commands
        pass

    def stop_balance_recovery(self):
        """Stop balance recovery procedure"""
        pass

# Main navigation behavior tree
def create_navigation_behavior_tree(goal_pose):
    """Create behavior tree for humanoid navigation"""
    # Root selector - try to navigate, but handle obstacles and balance
    root = SelectorNode("NavigationRoot", [
        # Higher priority: Emergency behaviors
        MonitorBalanceNode("BalanceMonitor"),

        # Main navigation task
        NavigateToGoalNode("NavigateToGoal", goal_pose),
    ])

    # More complex tree with obstacle avoidance
    complex_root = SelectorNode("ComplexNavigation", [
        MonitorBalanceNode("BalanceMonitor"),

        SequenceNode("NavigateWithAvoidance", [
            AvoidObstaclesNode("CheckObstacles"),
            NavigateToGoalNode("NavigateToGoal", goal_pose)
        ])
    ])

    return complex_root
```

## Autonomous Navigation Implementation

Implementing complete autonomous navigation for humanoid robots requires integrating all the components we've discussed: perception, path planning, control, and AI-driven decision making. This section provides a comprehensive implementation of autonomous navigation system.

### Complete Navigation System Architecture

```python
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PoseWithCovarianceStamped, Twist, PoseStamped
from nav_msgs.msg import Path, Odometry
from sensor_msgs.msg import LaserScan, Image, Imu
from std_msgs.msg import String, Bool
from visualization_msgs.msg import Marker, MarkerArray
from tf2_ros import TransformListener, Buffer
import tf2_geometry_msgs
import numpy as np
from scipy.spatial.transform import Rotation as R
import threading
import time

class HumanoidNavigationSystem(Node):
    def __init__(self):
        super().__init__('humanoid_navigation_system')

        # Initialize components
        self.global_planner = HumanoidGlobalPlanner()
        self.local_planner = HumanoidLocalPlanner()
        self.ai_controller = AIHumanoidController()
        self.terrain_aware_nav = TerrainAwareNavigation()

        # Navigation state
        self.current_pose = None
        self.current_goal = None
        self.current_path = None
        self.navigation_active = False
        self.navigation_mode = "IDLE"  # IDLE, PLANNING, EXECUTING, RECOVERY

        # Subscribers
        self.pose_sub = self.create_subscription(
            PoseWithCovarianceStamped,
            '/amcl_pose',
            self.pose_callback,
            10
        )

        self.odom_sub = self.create_subscription(
            Odometry,
            '/odom',
            self.odom_callback,
            10
        )

        self.scan_sub = self.create_subscription(
            LaserScan,
            '/scan',
            self.scan_callback,
            10
        )

        self.imu_sub = self.create_subscription(
            Imu,
            '/imu/data',
            self.imu_callback,
            10
        )

        self.goal_sub = self.create_subscription(
            PoseStamped,
            '/move_base_simple/goal',
            self.goal_callback,
            10
        )

        self.camera_sub = self.create_subscription(
            Image,
            '/camera/image_raw',
            self.camera_callback,
            10
        )

        # Publishers
        self.cmd_vel_pub = self.create_publisher(Twist, '/cmd_vel', 10)
        self.path_pub = self.create_publisher(Path, '/navigation_path', 10)
        self.status_pub = self.create_publisher(String, '/navigation_status', 10)
        self.marker_pub = self.create_publisher(MarkerArray, '/navigation_markers', 10)

        # TF listener
        self.tf_buffer = Buffer()
        self.tf_listener = TransformListener(self.tf_buffer, self)

        # Timers
        self.navigation_timer = self.create_timer(0.1, self.navigation_control_loop)  # 10 Hz
        self.ai_update_timer = self.create_timer(0.05, self.ai_update_loop)  # 20 Hz

        # Threading for heavy computations
        self.planning_thread = None
        self.planning_lock = threading.Lock()

        self.get_logger().info('Humanoid Navigation System initialized')

    def pose_callback(self, msg):
        """Handle pose updates from localization"""
        self.current_pose = msg.pose.pose
        self.publish_navigation_markers()

    def odom_callback(self, msg):
        """Handle odometry updates"""
        self.current_velocity = msg.twist.twist

    def scan_callback(self, msg):
        """Handle laser scan data"""
        self.laser_scan = msg
        # Process scan for obstacle detection
        self.detect_obstacles_from_scan(msg)

    def imu_callback(self, msg):
        """Handle IMU data for balance monitoring"""
        self.imu_data = msg
        # Check balance based on IMU data
        self.check_balance_from_imu(msg)

    def goal_callback(self, msg):
        """Handle new navigation goal"""
        self.current_goal = msg.pose
        self.navigation_mode = "PLANNING"
        self.get_logger().info(f'New goal received: ({msg.pose.position.x:.2f}, {msg.pose.position.y:.2f})')

        # Start path planning in separate thread to avoid blocking
        self.planning_thread = threading.Thread(target=self.plan_path_threaded)
        self.planning_thread.start()

    def camera_callback(self, msg):
        """Handle camera images for terrain classification"""
        self.camera_image = msg
        # Process image for terrain classification (non-blocking)
        threading.Thread(target=self.process_camera_image, args=(msg,)).start()

    def plan_path_threaded(self):
        """Run path planning in a separate thread"""
        with self.planning_lock:
            if self.current_pose and self.current_goal:
                try:
                    # Plan path using humanoid-aware planner
                    path = self.global_planner.create_plan(
                        self.current_pose,
                        self.current_goal,
                        self.get_costmap()  # This would come from costmap server
                    )

                    if path is not None:
                        self.current_path = path
                        self.navigation_mode = "EXECUTING"
                        self.navigation_active = True

                        # Publish the planned path
                        self.publish_path(path)

                        self.get_logger().info('Path planning completed successfully')
                    else:
                        self.get_logger().warn('Path planning failed - no valid path found')
                        self.navigation_mode = "IDLE"

                except Exception as e:
                    self.get_logger().error(f'Path planning error: {e}')
                    self.navigation_mode = "IDLE"

    def navigation_control_loop(self):
        """Main navigation control loop"""
        if not self.navigation_active or not self.current_pose:
            return

        # Update navigation status
        status_msg = String()

        if self.navigation_mode == "EXECUTING":
            # Execute the planned path
            velocity_cmd = self.execute_path()

            if velocity_cmd:
                self.cmd_vel_pub.publish(velocity_cmd)
                status_msg.data = "EXECUTING_PATH"
            else:
                # Path execution completed or failed
                self.navigation_mode = "IDLE"
                self.navigation_active = False
                status_msg.data = "PATH_COMPLETED"

        elif self.navigation_mode == "PLANNING":
            status_msg.data = "PLANNING_PATH"

        elif self.navigation_mode == "RECOVERY":
            # Execute recovery behavior
            recovery_cmd = self.execute_recovery()
            if recovery_cmd:
                self.cmd_vel_pub.publish(recovery_cmd)
            status_msg.data = "RECOVERY_MODE"

        else:
            status_msg.data = "IDLE"

        self.status_pub.publish(status_msg)

    def ai_update_loop(self):
        """AI-driven updates to navigation behavior"""
        if not self.current_pose or not self.navigation_active:
            return

        # Prepare sensor data for AI controller
        sensor_data = self.collect_sensor_data()

        # Update AI controller (this will adjust gait and navigation parameters)
        gait_commands = self.ai_controller.update_navigation(sensor_data, 0.05)  # 20Hz update

        # Use gait commands to influence navigation behavior
        self.apply_gait_commands_to_navigation(gait_commands)

    def execute_path(self):
        """Execute the current planned path"""
        if not self.current_path or not self.current_pose:
            return None

        # Check if we've reached the goal
        if self.has_reached_goal():
            self.navigation_active = False
            self.navigation_mode = "IDLE"
            return None

        # Compute local velocity command to follow the path
        try:
            velocity_cmd = self.local_planner.compute_velocity_commands(
                self.current_pose,
                self.current_velocity if hasattr(self, 'current_velocity') else None,
                self.current_goal,
                self.current_path
            )

            # Check for obstacles and adjust if needed
            if hasattr(self, 'obstacles') and self.obstacles:
                velocity_cmd = self.adjust_for_obstacles(velocity_cmd, self.obstacles)

            return velocity_cmd

        except Exception as e:
            self.get_logger().error(f'Error executing path: {e}')
            self.navigation_mode = "RECOVERY"
            return self.get_recovery_command()

    def has_reached_goal(self):
        """Check if robot has reached the navigation goal"""
        if not self.current_pose or not self.current_goal:
            return False

        dx = self.current_goal.position.x - self.current_pose.position.x
        dy = self.current_goal.position.y - self.current_pose.position.y
        distance = (dx*dx + dy*dy)**0.5

        # Check both position and orientation
        position_ok = distance < 0.3  # 30cm tolerance

        # For orientation, check if we're facing roughly the right direction
        # This would require comparing robot's actual orientation with goal orientation
        orientation_ok = True  # Simplified for now

        return position_ok and orientation_ok

    def adjust_for_obstacles(self, original_cmd, obstacles):
        """Adjust velocity command to avoid obstacles"""
        # Simple obstacle avoidance - reduce speed when obstacles are detected
        min_distance = float('inf')

        for obstacle in obstacles:
            obs_distance = ((obstacle[0] - self.current_pose.position.x)**2 +
                           (obstacle[1] - self.current_pose.position.y)**2)**0.5
            min_distance = min(min_distance, obs_distance)

        if min_distance < 1.0:  # Obstacle within 1m
            # Reduce speed proportionally to proximity
            speed_reduction = max(0.1, min_distance / 1.0)
            adjusted_cmd = Twist()
            adjusted_cmd.linear.x = original_cmd.linear.x * speed_reduction
            adjusted_cmd.linear.y = original_cmd.linear.y * speed_reduction
            adjusted_cmd.angular.z = original_cmd.angular.z
            return adjusted_cmd

        return original_cmd

    def execute_recovery(self):
        """Execute recovery behavior when navigation fails"""
        # Simple recovery - stop and try to re-plan
        recovery_cmd = Twist()

        # If we're stuck, try to move back slightly
        if hasattr(self, 'stuck_detector') and self.stuck_detector:
            recovery_cmd.linear.x = -0.1  # Move backward slowly
            recovery_cmd.angular.z = 0.0
        else:
            # Stop completely
            recovery_cmd.linear.x = 0.0
            recovery_cmd.angular.z = 0.0

        # After some time, try to re-plan
        if self.get_clock().now().nanoseconds / 1e9 > self.recovery_start_time + 2.0:
            self.navigation_mode = "PLANNING"
            self.recovery_start_time = self.get_clock().now().nanoseconds / 1e9

        return recovery_cmd

    def get_recovery_command(self):
        """Get a basic recovery command"""
        cmd = Twist()
        cmd.linear.x = 0.0
        cmd.linear.y = 0.0
        cmd.angular.z = 0.0
        return cmd

    def detect_obstacles_from_scan(self, scan_msg):
        """Detect obstacles from laser scan"""
        ranges = np.array(scan_msg.ranges)
        angles = np.linspace(scan_msg.angle_min, scan_msg.angle_max, len(ranges))

        # Filter out invalid ranges
        valid_indices = (ranges > scan_msg.range_min) & (ranges < scan_msg.range_max)
        valid_ranges = ranges[valid_indices]
        valid_angles = angles[valid_indices]

        # Convert to Cartesian coordinates
        x_points = valid_ranges * np.cos(valid_angles)
        y_points = valid_ranges * np.sin(valid_angles)

        # Cluster points to identify obstacles
        obstacles = self.cluster_obstacle_points(x_points, y_points)
        self.obstacles = obstacles

    def cluster_obstacle_points(self, x_points, y_points):
        """Cluster laser scan points into obstacles"""
        obstacles = []

        # Simple clustering - group nearby points
        for i in range(len(x_points)):
            point = (x_points[i], y_points[i])

            # Check if point is near existing obstacle
            added_to_existing = False
            for j, obstacle in enumerate(obstacles):
                center_x, center_y = obstacle[0], obstacle[1]
                distance = ((point[0] - center_x)**2 + (point[1] - center_y)**2)**0.5

                if distance < 0.3:  # Within 30cm
                    # Update obstacle center (simple average)
                    count = obstacle[2] if len(obstacle) > 2 else 1
                    new_count = count + 1
                    obstacles[j] = [
                        (center_x * count + point[0]) / new_count,
                        (center_y * count + point[1]) / new_count,
                        new_count
                    ]
                    added_to_existing = True
                    break

            if not added_to_existing:
                obstacles.append([point[0], point[1], 1])  # x, y, count

        return obstacles

    def check_balance_from_imu(self, imu_msg):
        """Check balance status from IMU data"""
        # Convert quaternion to Euler angles
        quat = [imu_msg.orientation.x, imu_msg.orientation.y,
                imu_msg.orientation.z, imu_msg.orientation.w]

        rotation = R.from_quat(quat)
        euler = rotation.as_euler('xyz')

        # Check tilt angles
        roll_threshold = 0.3  # radians
        pitch_threshold = 0.3

        self.balance_ok = (abs(euler[0]) < roll_threshold and
                          abs(euler[1]) < pitch_threshold)

        if not self.balance_ok:
            self.get_logger().warn(f'Balance compromised: roll={euler[0]:.2f}, pitch={euler[1]:.2f}')
            self.navigation_mode = "RECOVERY"

    def process_camera_image(self, image_msg):
        """Process camera image for terrain classification"""
        # This would convert ROS Image to PIL Image and classify terrain
        # For now, we'll simulate the process
        pass

    def collect_sensor_data(self):
        """Collect all relevant sensor data for AI controller"""
        sensor_data = {
            'camera_image': getattr(self, 'camera_image', None),
            'laser_scan': getattr(self, 'laser_scan', None),
            'imu_data': getattr(self, 'imu_data', None),
            'current_pose': self.current_pose,
            'current_velocity': getattr(self, 'current_velocity', None),
            'obstacles': getattr(self, 'obstacles', []),
            'left_foot_pose': self.get_left_foot_pose(),
            'right_foot_pose': self.get_right_foot_pose(),
            'com_pose': self.get_com_pose()
        }
        return sensor_data

    def get_left_foot_pose(self):
        """Get estimated left foot pose (would come from forward kinematics)"""
        # Simplified estimation
        if self.current_pose:
            from geometry_msgs.msg import Point
            return Point(
                x=self.current_pose.position.x - 0.1,
                y=self.current_pose.position.y + 0.1,
                z=0.0
            )
        return Point(x=0.0, y=0.0, z=0.0)

    def get_right_foot_pose(self):
        """Get estimated right foot pose (would come from forward kinematics)"""
        # Simplified estimation
        if self.current_pose:
            from geometry_msgs.msg import Point
            return Point(
                x=self.current_pose.position.x + 0.1,
                y=self.current_pose.position.y - 0.1,
                z=0.0
            )
        return Point(x=0.0, y=0.0, z=0.0)

    def get_com_pose(self):
        """Get estimated center of mass pose"""
        if self.current_pose:
            from geometry_msgs.msg import Point
            return Point(
                x=self.current_pose.position.x,
                y=self.current_pose.position.y,
                z=0.85  # Typical CoM height for humanoid
            )
        return Point(x=0.0, y=0.0, z=0.85)

    def apply_gait_commands_to_navigation(self, gait_commands):
        """Apply gait commands to influence navigation behavior"""
        # This would adjust navigation parameters based on gait commands
        # For example, adjusting step size, timing, or balance parameters
        pass

    def publish_path(self, path):
        """Publish the planned path for visualization"""
        path_msg = Path()
        path_msg.header.frame_id = "map"
        path_msg.header.stamp = self.get_clock().now().to_msg()
        path_msg.poses = path.poses if hasattr(path, 'poses') else []
        self.path_pub.publish(path_msg)

    def publish_navigation_markers(self):
        """Publish visualization markers for navigation"""
        if not self.current_pose:
            return

        marker_array = MarkerArray()

        # Robot position marker
        robot_marker = Marker()
        robot_marker.header.frame_id = "map"
        robot_marker.header.stamp = self.get_clock().now().to_msg()
        robot_marker.ns = "navigation"
        robot_marker.id = 1
        robot_marker.type = Marker.SPHERE
        robot_marker.action = Marker.ADD
        robot_marker.pose = self.current_pose
        robot_marker.scale.x = 0.3
        robot_marker.scale.y = 0.3
        robot_marker.scale.z = 0.3
        robot_marker.color.a = 1.0
        robot_marker.color.r = 0.0
        robot_marker.color.g = 1.0
        robot_marker.color.b = 0.0
        marker_array.markers.append(robot_marker)

        # Goal position marker (if exists)
        if self.current_goal:
            goal_marker = Marker()
            goal_marker.header.frame_id = "map"
            goal_marker.header.stamp = self.get_clock().now().to_msg()
            goal_marker.ns = "navigation"
            goal_marker.id = 2
            goal_marker.type = Marker.CYLINDER
            goal_marker.action = Marker.ADD
            goal_marker.pose = self.current_goal
            goal_marker.scale.x = 0.5
            goal_marker.scale.y = 0.5
            goal_marker.scale.z = 0.1
            goal_marker.color.a = 1.0
            goal_marker.color.r = 1.0
            goal_marker.color.g = 0.0
            goal_marker.color.b = 0.0
            marker_array.markers.append(goal_marker)

        self.marker_pub.publish(marker_array)

    def get_costmap(self):
        """Get costmap for path planning (placeholder)"""
        # In practice, this would interface with costmap_2d
        class MockCostmap:
            def get_costmap(self):
                return None
        return MockCostmap()

def main(args=None):
    rclpy.init(args=args)

    navigation_system = HumanoidNavigationSystem()

    try:
        rclpy.spin(navigation_system)
    except KeyboardInterrupt:
        navigation_system.get_logger().info('Navigation system shutting down')
    finally:
        navigation_system.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
```

### Navigation Configuration and Launch Files

#### 1. Navigation Parameters Configuration

```yaml
# humanoid_nav2_params.yaml
amcl:
  ros__parameters:
    use_sim_time: false
    alpha1: 0.2
    alpha2: 0.2
    alpha3: 0.2
    alpha4: 0.2
    alpha5: 0.2
    base_frame_id: "base_link"
    beam_skip_distance: 0.5
    beam_skip_error_threshold: 0.9
    beam_skip_threshold: 0.3
    do_beamskip: false
    global_frame_id: "map"
    lambda_short: 0.1
    laser_likelihood_max_dist: 2.0
    laser_max_range: 100.0
    laser_min_range: -1.0
    laser_model_type: "likelihood_field"
    max_beams: 60
    max_particles: 2000
    min_particles: 500
    odom_frame_id: "odom"
    pf_err: 0.05
    pf_z: 0.99
    recovery_alpha_fast: 0.0
    recovery_alpha_slow: 0.0
    resample_interval: 1
    robot_model_type: "nav2_amcl::DifferentialMotionModel"
    save_pose_rate: 0.5
    sigma_hit: 0.2
    tf_broadcast: true
    transform_tolerance: 1.0
    update_min_a: 0.2
    update_min_d: 0.25
    z_hit: 0.5
    z_max: 0.05
    z_rand: 0.5
    z_short: 0.05
    scan_topic: scan

bt_navigator:
  ros__parameters:
    use_sim_time: false
    global_frame: map
    robot_base_frame: base_link
    odom_topic: /odom
    default_bt_xml_filename: "navigate_w_replanning_and_recovery.xml"
    plugin_lib_names:
    - nav2_compute_path_to_pose_action
    - nav2_follow_path_action
    - nav2_back_up_action
    - nav2_spin_action
    - nav2_wait_action
    - nav2_clear_costmap_service
    - nav2_is_stuck_condition
    - nav2_goal_reached_condition
    - nav2_goal_updated_condition
    - nav2_initial_pose_received_condition
    - nav2_reinitialize_global_localization_service
    - nav2_rate_controller
    - nav2_distance_controller
    - nav2_speed_controller
    - nav2_truncate_path_action
    - nav2_goal_updater_node
    - nav2_recovery_node
    - nav2_pipeline_sequence
    - nav2_round_robin_node
    - nav2_transform_available_condition
    - nav2_time_expired_condition
    - nav2_distance_traveled_condition

controller_server:
  ros__parameters:
    use_sim_time: false
    controller_frequency: 20.0
    min_x_velocity_threshold: 0.001
    min_y_velocity_threshold: 0.001
    min_theta_velocity_threshold: 0.001
    progress_checker_plugin: "progress_checker"
    goal_checker_plugin: "goal_checker"
    controller_plugins: ["FollowPath"]

    # Progress checker parameters
    progress_checker:
      plugin: "nav2_controller::SimpleProgressChecker"
      required_movement_radius: 0.5
      movement_time_allowance: 10.0

    # Goal checker parameters
    goal_checker:
      plugin: "nav2_controller::SimpleGoalChecker"
      xy_goal_tolerance: 0.25
      yaw_goal_tolerance: 0.25
      stateful: True

    # Humanoid-specific controller
    FollowPath:
      plugin: "humanoid_controller::HumanoidController"
      primary_controller: "humanoid_controller::FootstepController"

      humanoid_controller:
        plugin: "humanoid_controller::HumanoidController"
        max_step_length: 0.6
        min_step_width: 0.3
        max_step_height: 0.15
        com_height: 0.85
        balance_margin: 0.1

local_costmap:
  local_costmap:
    ros__parameters:
      update_frequency: 5.0
      publish_frequency: 2.0
      global_frame: odom
      robot_base_frame: base_link
      use_sim_time: false
      rolling_window: true
      width: 6
      height: 6
      resolution: 0.05
      origin_x: -3.0
      origin_y: -3.0
  local_costmap_client:
    ros__parameters:
      use_sim_time: false
  local_costmap_rclcpp_node:
    ros__parameters:
      use_sim_time: false

global_costmap:
  global_costmap:
    ros__parameters:
      update_frequency: 1.0
      publish_frequency: 1.0
      global_frame: map
      robot_base_frame: base_link
      use_sim_time: false
      rolling_window: false
  global_costmap_client:
    ros__parameters:
      use_sim_time: false
  global_costmap_rclcpp_node:
    ros__parameters:
      use_sim_time: false

planner_server:
  ros__parameters:
    expected_planner_frequency: 20.0
    planner_plugins: ["GridBased"]
    GridBased:
      plugin: "nav2_navfn_planner/NavfnPlanner"
      tolerance: 0.5
      use_astar: false
      allow_unknown: true
```

#### 2. Launch File for Complete Navigation System

```python
# launch/humanoid_navigation_launch.py
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription, GroupAction
from launch.conditions import IfCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node, SetParameter
from launch_ros.substitutions import FindPackageShare

def generate_launch_description():
    # Launch arguments
    use_sim_time = LaunchConfiguration('use_sim_time')
    params_file = LaunchConfiguration('params_file')
    autostart = LaunchConfiguration('autostart')
    use_composition = LaunchConfiguration('use_composition')
    container_name = LaunchConfiguration('container_name')

    # Paths
    pkg_nav2_bringup = FindPackageShare('nav2_bringup')
    pkg_humanoid_nav = FindPackageShare('humanoid_navigation')

    # Declare launch arguments
    declare_use_sim_time = DeclareLaunchArgument(
        'use_sim_time',
        default_value='false',
        description='Use simulation time if true'
    )

    declare_params_file = DeclareLaunchArgument(
        'params_file',
        default_value=PathJoinSubstitution([
            FindPackageShare('humanoid_navigation'),
            'params',
            'humanoid_nav2_params.yaml'
        ]),
        description='Full path to the ROS2 parameters file to use for all launched nodes'
    )

    declare_autostart = DeclareLaunchArgument(
        'autostart',
        default_value='true',
        description='Automatically startup the nav2 stack'
    )

    declare_use_composition = DeclareLaunchArgument(
        'use_composition',
        default_value='false',
        description='Whether to use composed bringup'
    )

    declare_container_name = DeclareLaunchArgument(
        'container_name',
        default_value='nav2_container',
        description='the name of conatiner that nodes will load in if use composition'
    )

    # Launch Nav2 with our custom parameters
    nav2_bringup_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            PathJoinSubstitution([
                pkg_nav2_bringup,
                'launch',
                'navigation_launch.py'
            ])
        ]),
        launch_arguments={
            'use_sim_time': use_sim_time,
            'params_file': params_file,
            'autostart': autostart,
            'use_composition': use_composition,
            'container_name': container_name
        }.items()
    )

    # Launch our custom humanoid navigation system
    humanoid_nav_system = Node(
        package='humanoid_navigation',
        executable='humanoid_navigation_system',
        name='humanoid_navigation_system',
        parameters=[{'use_sim_time': use_sim_time}],
        output='screen'
    )

    # Launch terrain classification node
    terrain_classifier = Node(
        package='humanoid_navigation',
        executable='terrain_classifier',
        name='terrain_classifier',
        parameters=[{'use_sim_time': use_sim_time}],
        output='screen'
    )

    # Launch AI gait controller
    ai_gait_controller = Node(
        package='humanoid_navigation',
        executable='ai_gait_controller',
        name='ai_gait_controller',
        parameters=[{'use_sim_time': use_sim_time}],
        output='screen'
    )

    # Create launch description
    ld = LaunchDescription()

    # Add launch arguments
    ld.add_action(declare_use_sim_time)
    ld.add_action(declare_params_file)
    ld.add_action(declare_autostart)
    ld.add_action(declare_use_composition)
    ld.add_action(declare_container_name)

    # Add nodes
    ld.add_action(nav2_bringup_launch)
    ld.add_action(humanoid_nav_system)
    ld.add_action(terrain_classifier)
    ld.add_action(ai_gait_controller)

    return ld
```

## Practical Examples

Hands-on examples demonstrating path planning and navigation for humanoid robots.

### Example 1: Basic Humanoid Navigation Setup

This example demonstrates how to set up a basic navigation system for a humanoid robot:

```bash
# Terminal 1: Start the robot simulation (or bring up real robot)
ros2 launch my_humanoid_robot bringup.launch.py

# Terminal 2: Start navigation system
ros2 launch humanoid_navigation humanoid_navigation_launch.py

# Terminal 3: Send a navigation goal
ros2 run nav2_msgs goal_pose.py --x 5.0 --y 3.0 --theta 0.0
```

### Example 2: Advanced Navigation with AI Integration

This example shows how to implement AI-driven navigation with terrain classification:

```python
#!/usr/bin/env python3
# ai_humanoid_navigation_demo.py

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PoseStamped
from std_msgs.msg import String
import time

class NavigationDemo(Node):
    def __init__(self):
        super().__init__('navigation_demo')

        # Publisher for navigation goals
        self.goal_pub = self.create_publisher(PoseStamped, '/goal_pose', 10)

        # Publisher for status
        self.status_pub = self.create_publisher(String, '/demo_status', 10)

        # Timer for demo sequence
        self.demo_timer = self.create_timer(5.0, self.run_demo_sequence)
        self.demo_step = 0

        self.get_logger().info('Navigation Demo initialized')

    def run_demo_sequence(self):
        """Run a sequence of navigation demonstrations"""
        locations = [
            {'x': 2.0, 'y': 1.0, 'theta': 0.0, 'name': 'Table 1'},
            {'x': 4.0, 'y': 3.0, 'theta': 1.57, 'name': 'Table 2'},
            {'x': 1.0, 'y': 4.0, 'theta': 3.14, 'name': 'Table 3'},
            {'x': 0.0, 'y': 0.0, 'theta': 0.0, 'name': 'Home Position'}
        ]

        if self.demo_step < len(locations):
            location = locations[self.demo_step]

            # Publish navigation goal
            goal_msg = self.create_goal_message(
                location['x'],
                location['y'],
                location['theta']
            )

            self.goal_pub.publish(goal_msg)

            status_msg = String()
            status_msg.data = f"Navigating to {location['name']} ({location['x']}, {location['y']})"
            self.status_pub.publish(status_msg)

            self.get_logger().info(f'Published goal to {location["name"]}')

            self.demo_step += 1
        else:
            # Demo sequence complete
            status_msg = String()
            status_msg.data = "Demo sequence complete"
            self.status_pub.publish(status_msg)

            # Stop the timer
            self.demo_timer.cancel()

    def create_goal_message(self, x, y, theta):
        """Create a PoseStamped goal message"""
        from geometry_msgs.msg import PoseStamped, Point, Quaternion

        goal = PoseStamped()
        goal.header.frame_id = 'map'
        goal.header.stamp = self.get_clock().now().to_msg()

        goal.pose.position.x = x
        goal.pose.position.y = y
        goal.pose.position.z = 0.0

        # Convert theta (yaw) to quaternion
        import math
        sin_half_theta = math.sin(theta / 2.0)
        cos_half_theta = math.cos(theta / 2.0)

        goal.pose.orientation.x = 0.0
        goal.pose.orientation.y = 0.0
        goal.pose.orientation.z = sin_half_theta
        goal.pose.orientation.w = cos_half_theta

        return goal

def main(args=None):
    rclpy.init(args=args)

    demo = NavigationDemo()

    try:
        rclpy.spin(demo)
    except KeyboardInterrupt:
        demo.get_logger().info('Demo interrupted by user')
    finally:
        demo.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
```

### Example 3: Custom Path Planner Integration

This example shows how to integrate a custom path planner with Nav2:

```python
#!/usr/bin/env python3
# custom_humanoid_planner.py

import rclpy
from rclpy.node import Node
from nav2_msgs.action import ComputePathToPose
from nav_msgs.msg import Path
from geometry_msgs.msg import PoseStamped
from geometry_msgs.msg import Point
from builtin_interfaces.msg import Duration
import numpy as np
from rclpy.action import ActionServer, GoalResponse, CancelResponse
from rclpy.duration import Duration as RclDuration

class CustomHumanoidPlanner(Node):
    def __init__(self):
        super().__init__('custom_humanoid_planner')

        # Action server for path computation
        self._action_server = ActionServer(
            self,
            ComputePathToPose,
            'compute_path_to_pose',
            execute_callback=self.execute_callback,
            goal_callback=self.goal_callback,
            cancel_callback=self.cancel_callback
        )

        self.get_logger().info('Custom Humanoid Planner initialized')

    def goal_callback(self, goal_request):
        """Accept or reject path computation goal requests"""
        self.get_logger().info('Received path computation request')
        return GoalResponse.ACCEPT

    def cancel_callback(self, goal_handle):
        """Accept or reject path computation cancel requests"""
        self.get_logger().info('Received cancel request')
        return CancelResponse.ACCEPT

    def execute_callback(self, goal_handle):
        """Compute path from start to goal considering humanoid constraints"""
        self.get_logger().info('Executing path computation')

        # Extract goal information
        goal_pose = goal_handle.request.goal
        start_pose = goal_handle.request.start
        planner_id = goal_handle.request.planner_id
        tolerance = goal_handle.request.tolerance

        # Plan path with humanoid constraints
        path = self.plan_humanoid_path(start_pose, goal_pose, tolerance)

        # Create result
        result = ComputePathToPose.Result()
        if path:
            result.path = path
            goal_handle.succeed()
            self.get_logger().info('Path computation succeeded')
        else:
            result.path = Path()
            goal_handle.abort()
            self.get_logger().info('Path computation failed')

        return result

    def plan_humanoid_path(self, start_pose, goal_pose, tolerance):
        """Plan path considering humanoid robot constraints"""
        # This is a simplified implementation
        # In practice, this would use the sophisticated planners we developed earlier

        path = Path()
        path.header.frame_id = 'map'
        path.header.stamp = self.get_clock().now().to_msg()

        # Calculate straight-line path first
        dx = goal_pose.position.x - start_pose.position.x
        dy = goal_pose.position.y - start_pose.position.y
        distance = (dx*dx + dy*dy)**0.5

        # Determine number of waypoints based on distance
        num_waypoints = max(5, int(distance / 0.5))  # At least 5 waypoints, 0.5m spacing

        # Generate waypoints along the path
        for i in range(num_waypoints + 1):
            ratio = i / num_waypoints
            waypoint = PoseStamped()
            waypoint.header.frame_id = 'map'
            waypoint.header.stamp = self.get_clock().now().to_msg()

            waypoint.pose.position.x = start_pose.position.x + ratio * dx
            waypoint.pose.position.y = start_pose.position.y + ratio * dy
            waypoint.pose.position.z = start_pose.position.z  # Maintain height

            # Interpolate orientation
            waypoint.pose.orientation = goal_pose.orientation

            # Apply humanoid-specific constraints
            if not self.is_waypoint_valid(waypoint.pose):
                # Try to find alternative route around obstacle
                waypoint = self.find_alternative_waypoint(waypoint, start_pose, goal_pose)
                if not waypoint:
                    return None  # Cannot find valid path

            path.poses.append(waypoint)

        # Post-process path to add humanoid-specific information
        path = self.add_humanoid_constraints(path)

        return path

    def is_waypoint_valid(self, pose):
        """Check if a waypoint is valid for humanoid navigation"""
        # In practice, this would check against costmap
        # For this example, we'll assume all waypoints are valid
        return True

    def find_alternative_waypoint(self, original_waypoint, start_pose, goal_pose):
        """Find alternative waypoint when original is invalid"""
        # This would implement local path adjustment
        # For now, return the original waypoint
        return original_waypoint

    def add_humanoid_constraints(self, path):
        """Add humanoid-specific constraints to path"""
        # Add metadata about step feasibility, balance constraints, etc.
        for i, pose_stamped in enumerate(path.poses):
            # Add humanoid-specific information as needed
            # This could include step timing, balance requirements, etc.
            pass

        return path

def main(args=None):
    rclpy.init(args=args)

    planner = CustomHumanoidPlanner()

    try:
        rclpy.spin(planner)
    except KeyboardInterrupt:
        planner.get_logger().info('Planner shutting down')
    finally:
        planner.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
```

### Example 4: Simulation Environment for Training

This example shows how to set up a simulation environment for training AI navigation systems:

```python
#!/usr/bin/env python3
# humanoid_navigation_sim.py

import gym
from gym import spaces
import numpy as np
import math

class HumanoidNavigationEnv(gym.Env):
    """Custom environment for training humanoid navigation policies"""

    def __init__(self):
        super(HumanoidNavigationEnv, self).__init__()

        # Define action and observation space
        # Actions: [left_foot_dx, left_foot_dy, right_foot_dx, right_foot_dy]
        self.action_space = spaces.Box(
            low=np.array([-0.3, -0.2, -0.3, -0.2]),
            high=np.array([0.3, 0.2, 0.3, 0.2]),
            dtype=np.float32
        )

        # Observations: [left_foot_x, left_foot_y, right_foot_x, right_foot_y,
        #                com_x, com_y, goal_x, goal_y, obstacle1_x, obstacle1_y,
        #                obstacle2_x, obstacle2_y, com_vel_x, com_vel_y]
        self.observation_space = spaces.Box(
            low=np.array([-10, -10, -10, -10, -10, -10, -10, -10, -10, -10, -10, -10, -2, -2]),
            high=np.array([10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 2, 2]),
            dtype=np.float32
        )

        # Environment parameters
        self.com_height = 0.85
        self.max_steps = 500
        self.step_count = 0
        self.reset()

    def reset(self, seed=None):
        """Reset the environment to initial state"""
        super().reset(seed=seed)

        # Initialize robot state
        self.left_foot = np.array([0.0, 0.1])
        self.right_foot = np.array([0.0, -0.1])
        self.com_pos = np.array([0.0, 0.0])
        self.com_vel = np.array([0.0, 0.0])

        # Set random goal
        self.goal = np.array([
            self.np_random.uniform(3, 8),
            self.np_random.uniform(-2, 2)
        ])

        # Set random obstacles
        self.obstacles = [
            np.array([self.np_random.uniform(1, 3), self.np_random.uniform(-1, 1)]),
            np.array([self.np_random.uniform(4, 6), self.np_random.uniform(-2, 0)])
        ]

        self.step_count = 0

        return self._get_observation(), {}

    def step(self, action):
        """Execute one step in the environment"""
        self.step_count += 1

        # Extract action components
        left_foot_action = action[:2]
        right_foot_action = action[2:]

        # Calculate new foot positions
        new_left_foot = self.left_foot + left_foot_action
        new_right_foot = self.right_foot + right_foot_action

        # Check if steps are valid (not in obstacles)
        if self._is_valid_step(new_left_foot) and self._is_valid_step(new_right_foot):
            # Update foot positions
            self.left_foot = new_left_foot
            self.right_foot = new_right_foot

            # Update CoM position (simplified - between feet)
            old_com = self.com_pos.copy()
            self.com_pos = (self.left_foot + self.right_foot) / 2

            # Update CoM velocity
            self.com_vel = (self.com_pos - old_com) / 0.1  # Assuming 0.1s per step

        # Calculate reward
        reward = self._calculate_reward()

        # Check if episode is done
        done = self._is_episode_done()

        # Get next observation
        observation = self._get_observation()

        info = {}

        return observation, reward, done, False, info

    def _is_valid_step(self, foot_pos):
        """Check if a footstep is valid (not in obstacles)"""
        for obs_pos in self.obstacles:
            dist = np.linalg.norm(foot_pos - obs_pos)
            if dist < 0.3:  # 30cm clearance
                return False
        return True

    def _calculate_reward(self):
        """Calculate reward for current state"""
        # Distance to goal (negative reward for distance)
        dist_to_goal = np.linalg.norm(self.com_pos - self.goal)
        reward = -dist_to_goal * 0.1

        # Bonus for getting closer to goal
        if dist_to_goal < 0.5:
            reward += 100  # Reached goal

        # Penalty for losing balance
        if not self._is_balanced():
            reward -= 10

        # Small penalty for time
        reward -= 0.01

        return reward

    def _is_balanced(self):
        """Check if robot is balanced (CoM over support polygon)"""
        # Create support polygon from feet positions
        min_x = min(self.left_foot[0], self.right_foot[0])
        max_x = max(self.left_foot[0], self.right_foot[0])
        min_y = min(self.left_foot[1], self.right_foot[1])
        max_y = max(self.left_foot[1], self.right_foot[1])

        # Check if CoM is within support polygon
        margin = 0.05
        return (min_x - margin <= self.com_pos[0] <= max_x + margin and
                min_y - margin <= self.com_pos[1] <= max_y + margin)

    def _is_episode_done(self):
        """Check if episode is done"""
        dist_to_goal = np.linalg.norm(self.com_pos - self.goal)

        return (dist_to_goal < 0.5 or  # Reached goal
                self.step_count >= self.max_steps or  # Max steps reached
                not self._is_balanced())  # Lost balance

    def _get_observation(self):
        """Get current observation"""
        obs = np.concatenate([
            self.left_foot,
            self.right_foot,
            self.com_pos,
            self.goal,
            self.obstacles[0],
            self.obstacles[1],
            self.com_vel
        ])
        return obs

def train_navigation_agent():
    """Train a navigation agent using the custom environment"""
    import torch
    import torch.nn as nn
    import torch.optim as optim

    # Create environment
    env = HumanoidNavigationEnv()

    # Simple neural network for policy
    class PolicyNet(nn.Module):
        def __init__(self):
            super(PolicyNet, self).__init__()
            self.network = nn.Sequential(
                nn.Linear(env.observation_space.shape[0], 128),
                nn.ReLU(),
                nn.Linear(128, 128),
                nn.ReLU(),
                nn.Linear(128, env.action_space.shape[0]),
                nn.Tanh()
            )

        def forward(self, x):
            return self.network(x)

    policy = PolicyNet()
    optimizer = optim.Adam(policy.parameters(), lr=0.001)

    # Training loop (simplified)
    for episode in range(1000):
        obs, _ = env.reset()
        total_reward = 0

        for step in range(500):  # Max steps per episode
            obs_tensor = torch.FloatTensor(obs)
            action = policy(obs_tensor).detach().numpy()

            next_obs, reward, done, _, _ = env.step(action)
            total_reward += reward

            if done:
                break

            obs = next_obs

        if episode % 100 == 0:
            print(f"Episode {episode}, Total Reward: {total_reward:.2f}")

if __name__ == '__main__':
    # Run training
    train_navigation_agent()
```

## Summary and Next Steps

In this chapter, we've explored the comprehensive implementation of path planning with Nav2 for humanoid robots. The key concepts and techniques covered include:

### Key Concepts Mastered
- **Nav2 Integration**: Understanding how to adapt the Nav2 navigation stack for humanoid robot requirements
- **Bipedal Motion Constraints**: Implementing navigation that respects the unique physical constraints of two-legged locomotion
- **Trajectory Planning Algorithms**: Developing specialized algorithms for planning both overall paths and detailed footstep sequences
- **AI-Driven Control**: Implementing intelligent control systems that adapt to changing environments and conditions
- **Autonomous Navigation**: Complete implementation of self-navigation capabilities for humanoid robots

### Technical Implementation Highlights
- Developed custom path planners that consider humanoid-specific constraints like step length, balance, and stability
- Implemented AI-driven control systems using reinforcement learning and neural networks
- Created comprehensive navigation systems that integrate perception, planning, and control
- Established proper integration with the Nav2 framework while maintaining humanoid-specific requirements
- Developed simulation environments for training and testing navigation policies

### Best Practices Established
- Used appropriate safety margins and balance constraints to ensure stable locomotion
- Implemented proper fallback behaviors for navigation failures
- Applied AI techniques to adapt navigation to different terrain types
- Established proper timing and coordination between different navigation components
- Created comprehensive testing and validation procedures for navigation systems

### Advanced Considerations
For production humanoid navigation systems, additional considerations include:

#### 1. Real-time Performance
- **Efficient Algorithms**: Optimize path planning algorithms for real-time execution
- **Predictive Control**: Implement predictive control to handle dynamic environments
- **Multi-rate Control**: Use different control rates for different aspects of navigation

#### 2. Robustness and Safety
- **Sensor Fusion**: Integrate multiple sensor modalities for robust perception
- **Failure Recovery**: Implement comprehensive failure detection and recovery procedures
- **Safe Learning**: Ensure AI systems learn safely without compromising robot stability

#### 3. Adaptation and Learning
- **Online Learning**: Implement systems that can adapt to new environments online
- **Transfer Learning**: Use simulation-to-reality transfer techniques
- **Multi-task Learning**: Train systems that can handle multiple navigation tasks

### Next Steps

With the foundation of Isaac Sim, Isaac ROS VSLAM, and Nav2 path planning established, the next phase of development should focus on:

- **Integration Testing**: Comprehensive testing of the complete perception-navigation pipeline
- **Real Robot Deployment**: Transitioning from simulation to real humanoid robot platforms
- **Advanced AI Techniques**: Implementing more sophisticated AI methods like imitation learning and meta-learning
- **Human-Robot Interaction**: Developing navigation systems that can operate safely around humans
- **Multi-Robot Coordination**: Extending to multi-robot navigation scenarios

The knowledge gained in this module provides the essential foundation for advanced humanoid robot navigation, combining simulation capabilities, perception systems, and intelligent path planning to create truly autonomous humanoid robots.

## Transition to Advanced AI Perception Techniques

As we conclude Module 3, it's important to understand how the concepts covered here connect to advanced AI perception techniques that form the next phase of development in humanoid robotics:

### Deep Learning for Perception
- **Semantic Segmentation**: Using deep neural networks to understand scene context and object relationships
- **Instance Segmentation**: Distinguishing between individual objects of the same class for more detailed scene understanding
- **Object Detection and Tracking**: Real-time identification and tracking of dynamic objects in the environment
- **Pose Estimation**: Determining the 6D pose of objects for manipulation and interaction

### Reinforcement Learning for Navigation
- **End-to-End Learning**: Training complete navigation policies directly from sensor data to actions
- **Sim-to-Real Transfer**: Techniques for transferring policies trained in simulation to real robots
- **Multi-Task Learning**: Training agents that can handle multiple navigation and manipulation tasks
- **Curriculum Learning**: Progressive training from simple to complex navigation scenarios

### Advanced SLAM Techniques
- **Semantic SLAM**: Incorporating object-level understanding into mapping and localization
- **Dynamic SLAM**: Handling moving objects and dynamic environments
- **Collaborative SLAM**: Multi-robot systems sharing mapping information
- **Long-term Mapping**: Maintaining and updating maps over extended periods

### Next Module Preview
Module 4 will explore these advanced AI perception techniques, diving deep into:
- Deep learning architectures optimized for robotic perception
- Techniques for efficient sim-to-real transfer
- Advanced sensor fusion methods
- Multi-modal perception systems
- Human-aware navigation and social robotics

The foundation built in this module with Isaac Sim, Isaac ROS VSLAM, and Nav2 path planning provides the essential tools and understanding needed to tackle these advanced topics.

### Navigation
- **Previous**: [Chapter 2: Isaac ROS & VSLAM](./chapter2-isaac-ros-vslam)
- **Next**: [Module 3 Conclusion](./index)
