import { notFound } from 'next/navigation';

// Mock content data - in a real app, this would come from your backend
const mockContentData: Record<string, { title: string; content: string }> = {
  module1: {
    title: 'The Robotic Nervous System (ROS 2)',
    content: `
# The Robotic Nervous System (ROS 2)

## Introduction

Robot Operating System 2 (ROS 2) is a flexible framework for writing robot software. It's a collection of tools, libraries, and conventions that aim to simplify the task of creating complex and robust robot behavior across a wide variety of robot platforms.

## Key Concepts

- **Nodes**: A node is a process that performs computation. ROS 2 is designed to have many nodes running at the same time.
- **Topics**: Nodes exchange messages by publishing to and subscribing to topics.
- **Services**: Services provide a request/response interaction between nodes.
- **Actions**: Actions are similar to services but designed for long-running tasks.

## Practical Applications

ROS 2 is used in a variety of applications, from research robots to commercial products. Its modular design allows for easy integration of new capabilities and reuse of existing code.
    `
  },
  module2: {
    title: 'The Digital Twin (Gazebo & Unity)',
    content: `
# The Digital Twin (Gazebo & Unity)

## Introduction

A digital twin in robotics is a virtual representation of a physical robot and its environment. Simulation environments like Gazebo and Unity allow developers to test algorithms safely and efficiently before deploying them to real robots.

## Gazebo Simulation

Gazebo provides realistic physics simulation, high-quality graphics, and convenient programmatic interfaces. It's widely used in robotics research and development.

## Unity Robotics

Unity offers a powerful 3D development platform with high-fidelity rendering and a large asset library. Unity Robotics Hub provides tools for developing, training, and testing robotic systems in simulation.

## Benefits of Simulation

- Safety: Test algorithms without risk to hardware or humans
- Cost-effectiveness: Reduce need for physical prototypes
- Reproducibility: Create controlled testing conditions
- Speed: Run simulations faster than real-time
    `
  },
  module3: {
    title: 'The AI-Robot Brain (NVIDIA Isaac™)',
    content: `
# The AI-Robot Brain (NVIDIA Isaac™)

## Introduction

NVIDIA Isaac is a comprehensive robotics platform that provides the software and tools needed to build, simulate, and deploy AI-powered robots. It leverages NVIDIA's GPU computing platform to accelerate AI workloads.

## Key Components

- **Isaac ROS**: Hardware-accelerated packages for robotics
- **Isaac Sim**: High-fidelity simulation environment
- **Isaac Apps**: Reference applications for common robotics tasks

## AI Capabilities

Modern robots need to perceive their environment, make decisions, and act accordingly. NVIDIA Isaac provides tools for computer vision, path planning, and manipulation that enable robots to perform complex tasks.

## Deep Learning Integration

Isaac supports popular deep learning frameworks and provides pre-trained models that can be customized for specific applications.
    `
  },
  module4: {
    title: 'Vision-Language-Action (VLA)',
    content: `
# Vision-Language-Action (VLA)

## Introduction

Vision-Language-Action (VLA) models represent a new paradigm in robotics where perception, language understanding, and action execution are unified in a single model. This approach enables robots to understand complex instructions and act in unstructured environments.

## Perception

Robots must accurately perceive their environment using cameras, lidar, and other sensors. Computer vision techniques enable robots to identify objects, understand spatial relationships, and navigate safely.

## Language Understanding

Natural language processing allows robots to understand human commands and provide feedback in human-readable form. This is crucial for human-robot interaction.

## Action Execution

Converting high-level goals into low-level motor commands requires sophisticated planning and control algorithms. Modern approaches leverage machine learning to improve performance in varied environments.

## Integration Challenges

Successfully combining vision, language, and action requires careful system design and often involves trade-offs between accuracy, speed, and computational requirements.
    `
  },
  'lesson1-1': {
    title: 'Introduction to ROS 2',
    content: `
# Introduction to ROS 2

## What is ROS 2?

Robot Operating System 2 (ROS 2) is not an operating system but rather a collection of software libraries and tools that help you build robot applications. It provides hardware abstraction, device drivers, libraries, visualizers, message-passing, package management, and more.

## Why ROS 2?

ROS 2 was developed to address the limitations of ROS 1 and to enable the development of commercial robot applications. Key improvements include:

- Improved real-time support
- Better security features
- Support for multiple operating systems
- Professional support and maintenance

## Basic Architecture

ROS 2 uses a DDS (Data Distribution Service) implementation for communication between nodes. This provides better scalability and reliability compared to the ROS 1 master-based system.

## Getting Started

To get started with ROS 2, you'll need to install it on your system and learn the basic command-line tools for creating and managing packages, nodes, and topics.
    `
  },
  'lesson1-2': {
    title: 'Nodes and Topics',
    content: `
# Nodes and Topics

## Nodes

In ROS 2, a node is a process that performs computation. Nodes are the fundamental building blocks of a ROS 2 program. You can think of a node as a single executable that uses ROS services.

## Topics

Topics are named buses over which nodes exchange messages. A node can publish messages to a topic or subscribe to messages from a topic. This is the basis for the publish/subscribe communication model in ROS.

## Publisher-Subscriber Pattern

The publisher-subscriber pattern allows for asynchronous communication between nodes. Publishers send messages to topics without knowing who (if anyone) is subscribed. Subscribers receive messages from topics without knowing who (if anyone) is publishing.

## Creating Nodes

To create a node in ROS 2, you typically:
1. Create a new package
2. Define the node class
3. Initialize the node
4. Create publishers/subscribers
5. Spin the node to process callbacks
    `
  },
  'lesson1-3': {
    title: 'Services and Actions',
    content: `
# Services and Actions

## Services

Services provide a request/response communication pattern in ROS 2. When a node sends a request to a service, it waits for a response. This is different from the asynchronous publish/subscribe model used by topics.

## Service Architecture

A service has:
- A client that sends requests
- A server that receives requests and sends responses
- A service definition that specifies the request and response types

## Actions

Actions are similar to services but designed for long-running tasks. They support:
- Feedback during execution
- Result reporting
- Goal preemption
- Canceling in-progress goals

## When to Use What

- Use topics for continuous data streams
- Use services for simple request/response operations
- Use actions for long-running operations that need feedback
    `
  },
  weekly_breakdown: {
    title: 'Weekly Course Breakdown',
    content: `
# Weekly Course Breakdown

## Week 1-3: The Robotic Nervous System (ROS 2)
- Introduction to ROS 2 concepts
- Nodes, topics, services, and actions
- Building your first ROS 2 package
- Robot simulation with Gazebo

## Week 4-6: The Digital Twin (Gazebo & Unity)
- Simulation environments for robotics
- Physics engines and realistic rendering
- Unity Robotics integration
- Testing algorithms in simulation

## Week 7-9: The AI-Robot Brain (NVIDIA Isaac™)
- Introduction to NVIDIA Isaac platform
- Perception systems and computer vision
- Path planning and navigation
- Manipulation and control

## Week 10-12: Vision-Language-Action (VLA)
- Multimodal AI for robotics
- Language understanding in robotics
- Vision-language models
- End-to-end robot learning
    `
  },
  assessments: {
    title: 'Assessments',
    content: `
# Assessments

## Weekly Quizzes
- Short quizzes to test understanding of key concepts
- Multiple choice and short answer questions
- Due each Sunday at 11:59 PM

## Programming Assignments
- Hands-on implementation of concepts learned
- Simulation-based projects using Gazebo
- Due every other Friday

## Midterm Project
- Develop a complete robotic system using ROS 2
- Implement perception, planning, and control
- Due Week 6

## Final Project
- Capstone project integrating all course concepts
- Work in teams of 2-3 students
- Present to class in Week 12
    `
  },
  hardware: {
    title: 'Hardware Guide',
    content: `
# Hardware Guide

## Required Components

### Robot Platform
- Mobile base with differential drive
- Onboard computer (NVIDIA Jetson recommended)
- IMU and wheel encoders for odometry

### Sensors
- RGB-D camera (Intel RealSense D435)
- 2D LIDAR (Hokuyo URG-04LX-UG01)
- IMU for orientation

### Actuators
- Servos for manipulation (if applicable)
- Motors for locomotion

## Optional Components
- External GPU for AI processing
- Additional cameras for redundancy
- Battery management system

## Assembly Instructions
Detailed assembly instructions are provided in the lab manual.
    `
  },
  capstone: {
    title: 'Capstone Project',
    content: `
# Capstone Project

## Project Overview
The capstone project is a team-based project where you'll implement a complete robotic system that integrates all concepts learned in the course.

## Project Requirements
- Navigate to a specified location in an unknown environment
- Identify and manipulate specific objects
- Respond to voice commands
- Adapt to changing conditions

## Timeline
- Project proposal: Week 7
- Mid-project presentation: Week 9
- Final presentation: Week 12
- Final report: Due Week 13

## Evaluation Criteria
- Technical implementation (40%)
- Innovation and creativity (20%)
- Teamwork and collaboration (20%)
- Presentation and documentation (20%)
    `
  }
};

export default function TextbookContentPage({ params }: { params: { slug: string } }) {
  const content = mockContentData[params.slug];

  if (!content) {
    notFound();
  }

  // In a real application, you would fetch this content from your backend
  // and potentially render it using a markdown parser or similar

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow">
        <div className="max-w-7xl mx-auto px-4 py-6 sm:px-6 lg:px-8 flex justify-between items-center">
          <h1 className="text-2xl font-bold text-gray-900">Physical AI & Humanoid Robotics</h1>
          <div className="flex items-center space-x-4">
            <button className="text-gray-600 hover:text-gray-900">
              <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
              </svg>
            </button>
            <button className="text-gray-600 hover:text-gray-900">
              <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8.684 13.342C8.886 12.938 9 12.482 9 12c0-.482-.114-.938-.316-1.342m0 2.684a3 3 0 110-2.684m0 2.684l6.632 3.316m-6.632-6l6.632-3.316m0 0a3 3 0 105.367-2.684 3 3 0 00-5.367 2.684zm0 9.316a3 3 0 105.368 2.684 3 3 0 00-5.368-2.684z" />
              </svg>
            </button>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 py-6 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center mb-6">
          <h1 className="text-3xl font-bold text-gray-900">{content.title}</h1>
          <div className="flex space-x-2">
            <button className="bg-blue-500 text-white px-4 py-2 rounded-lg hover:bg-blue-600 text-sm">
              Urdu Translation
            </button>
            <button className="bg-white border border-gray-300 text-gray-700 px-4 py-2 rounded-lg hover:bg-gray-50 text-sm">
              Personalize
            </button>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow-md overflow-hidden">
          <div className="p-8 prose max-w-none">
            {content.content.split('\n\n').map((paragraph, index) => {
              if (paragraph.startsWith('# ')) {
                return <h1 key={index} className="text-2xl font-bold text-gray-900 mt-8 mb-4">{paragraph.substring(2)}</h1>;
              } else if (paragraph.startsWith('## ')) {
                return <h2 key={index} className="text-xl font-semibold text-gray-900 mt-6 mb-3">{paragraph.substring(3)}</h2>;
              } else if (paragraph.startsWith('### ')) {
                return <h3 key={index} className="text-lg font-medium text-gray-900 mt-4 mb-2">{paragraph.substring(4)}</h3>;
              } else if (paragraph.trim() !== '') {
                return <p key={index} className="text-gray-700 mb-4">{paragraph}</p>;
              }
              return null;
            })}
          </div>
        </div>

        <div className="mt-8 flex justify-between">
          <button className="text-blue-600 hover:text-blue-800 font-medium">
            ← Previous Lesson
          </button>
          <button className="bg-blue-500 text-white px-6 py-2 rounded-lg hover:bg-blue-600">
            Next Lesson →
          </button>
        </div>
      </main>
    </div>
  );
}