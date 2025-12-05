# Module 1: The Robotic Nervous System (ROS 2)

## Overview

In this module, we explore the foundation of modern robotics: the Robot Operating System 2 (ROS 2). Think of ROS 2 as the "nervous system" of a robot—it connects all the components, manages communication between different parts, and provides the infrastructure for complex robotic behaviors.

## Learning Objectives

By the end of this module, students will be able to:
- Understand ROS 2 architecture and core concepts
- Create and manage ROS 2 nodes, topics, and services
- Build ROS 2 packages with Python
- Bridge Python AI agents to ROS controllers using rclpy
- Understand URDF (Unified Robot Description Format) for humanoids

## Table of Contents

1. [Introduction to ROS 2](#introduction-to-ros-2)
2. [Core Concepts: Nodes, Topics, and Services](#core-concepts)
3. [Building ROS 2 Packages](#building-ros-2-packages)
4. [Python Integration with rclpy](#python-integration-with-rclpy)
5. [URDF for Humanoid Robots](#urdf-for-humanoid-robots)
6. [Practical Exercises](#practical-exercises)

## Introduction to ROS 2

ROS 2 (Robot Operating System 2) is not an operating system but rather a flexible framework for writing robot software. It provides services designed for a heterogeneous computer cluster such as hardware abstraction, device drivers, libraries, visualizers, message-passing, package management, and more.

### Key Differences from ROS 1

- **Quality of Service (QoS)**: ROS 2 introduces QoS policies for fine-grained control over message delivery
- **Real-Time Support**: Better real-time capabilities for safety-critical applications
- **Security**: Built-in security features for industrial and commercial use
- **DDS-Based**: Uses Data Distribution Service (DDS) as the underlying middleware

## Core Concepts

### Nodes
Nodes are processes that perform computation. ROS 2 is designed to be modular, with each node performing a specific function. For example, one node might handle camera input, another might process sensor data, and another might control actuators.

### Topics
Topics are named buses over which nodes exchange messages. A node can publish messages to a topic, and other nodes can subscribe to that topic to receive the messages. This creates a publisher-subscriber communication pattern.

### Services
Services provide a request-response communication pattern. A node can offer a service, and other nodes can call that service to request specific actions.

### Actions
Actions are similar to services but are designed for long-running tasks. They include feedback during execution and the ability to cancel ongoing tasks.

## Building ROS 2 Packages

A ROS 2 package is a reusable software module that contains nodes, libraries, and other resources. Here's the basic structure:

```
my_robot_package/
├── CMakeLists.txt
├── package.xml
├── src/
│   └── my_node.cpp
├── include/
│   └── my_robot_package/
│       └── my_header.hpp
├── launch/
│   └── my_launch_file.py
└── config/
    └── my_params.yaml
```

### Creating a Package

```bash
ros2 pkg create --build-type ament_python my_robot_package
```

## Python Integration with rclpy

rclpy is the Python client library for ROS 2. It provides the interface between Python applications and the ROS 2 system.

### Basic Node Structure

```python
import rclpy
from rclpy.node import Node

class MyRobotNode(Node):
    def __init__(self):
        super().__init__('my_robot_node')
        # Initialize publishers, subscribers, services here

def main(args=None):
    rclpy.init(args=args)
    node = MyRobotNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

### Publishers and Subscribers

```python
# Publisher
publisher = self.create_publisher(String, 'topic_name', 10)

# Subscriber
subscriber = self.create_subscription(
    String,
    'topic_name',
    self.topic_callback,
    10
)

def topic_callback(self, msg):
    self.get_logger().info(f'Received: {msg.data}')
```

## URDF for Humanoid Robots

URDF (Unified Robot Description Format) is an XML format for representing a robot model. For humanoid robots, URDF describes the physical structure, joints, and connections between different body parts.

### Basic URDF Structure

```xml
<?xml version="1.0"?>
<robot name="humanoid_robot">
  <!-- Links define rigid bodies -->
  <link name="base_link">
    <visual>
      <geometry>
        <box size="0.5 0.5 0.5"/>
      </geometry>
    </visual>
    <collision>
      <geometry>
        <box size="0.5 0.5 0.5"/>
      </geometry>
    </collision>
  </link>

  <!-- Joints connect links -->
  <joint name="hip_joint" type="revolute">
    <parent link="base_link"/>
    <child link="torso_link"/>
    <axis xyz="0 0 1"/>
    <limit lower="-1.57" upper="1.57" effort="100" velocity="1"/>
  </joint>

  <link name="torso_link">
    <visual>
      <geometry>
        <box size="0.3 0.3 0.8"/>
      </geometry>
    </visual>
  </link>
</robot>
```

### URDF for Humanoid Features

Humanoid robots require special considerations in URDF:
- **Degrees of Freedom**: Each limb should have sufficient joints for realistic movement
- **Mass Distribution**: Accurate masses and inertias for stable simulation
- **Collision Models**: Proper collision geometry for physics simulation
- **Materials**: Visual properties for rendering

## Practical Exercises

### Exercise 1: Create a Simple ROS 2 Node
Create a ROS 2 node that publishes messages to a topic and subscribes to another topic.

### Exercise 2: URDF Robot Model
Design a simple humanoid robot model in URDF with at least 10 joints.

### Exercise 3: ROS 2 Launch File
Create a launch file that starts multiple nodes simultaneously.

## Fun Facts

:::info{.fun-fact}
**Did you know?** The original ROS (Robot Operating System) was released in 2010 and revolutionized robotics research by providing standardized tools and interfaces. ROS 2, released in 2014, addressed many limitations of the original system.
:::

:::info{.fun-fact}
**Robotic Curiosity**: The "turtle" in the famous ROS turtlesim tutorial was inspired by Logo programming language's turtle graphics, which has been teaching programming concepts since the 1960s!
:::

## Assessment

Complete the following to demonstrate your understanding:
1. Create a ROS 2 package with a publisher and subscriber
2. Design a URDF model for a simple humanoid robot
3. Explain the differences between ROS 1 and ROS 2 in your own words

## Next Steps

After completing this module, continue to [Module 2: The Digital Twin (Gazebo & Unity)](/textbook/module2) to learn about robot simulation and environment building.