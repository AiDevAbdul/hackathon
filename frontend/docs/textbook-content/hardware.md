# Hardware Requirements

## Overview

The Physical AI and Humanoid Robotics course is technically demanding, requiring specialized hardware to support the computational loads of physics simulation, visual perception, and generative AI. This document outlines the required and recommended hardware configurations for successful course completion.

## Computational Demands

This course sits at the intersection of three computationally intensive domains:

1. **Physics Simulation** (Isaac Sim/Gazebo): Real-time physics calculations, collision detection, and rendering
2. **Visual Perception** (SLAM/Computer Vision): Real-time image processing, feature extraction, and neural network inference
3. **Generative AI** (LLMs/VLA): Large language model processing and multimodal AI operations

These combined demands require high-performance computing resources that exceed standard laptop capabilities.

## Required Hardware Configuration

### The "Digital Twin" Workstation (Required per Student)

This is the most critical component. NVIDIA Isaac Sim is an Omniverse application that requires "RTX" (Ray Tracing) capabilities. Standard laptops (MacBooks or non-RTX Windows machines) will not function adequately.

#### Minimum Specifications
- **GPU**: NVIDIA RTX 4070 Ti (12GB VRAM) or higher
  - *Why*: High VRAM needed to load USD assets for robots and environments while running VLA models simultaneously
  - *Alternative*: RTX 3080 (10GB VRAM) - may work but with reduced performance

- **CPU**: Intel Core i7 (13th Gen+) or AMD Ryzen 7 (7000 series)
  - *Why*: Physics calculations in Gazebo/Isaac are CPU-intensive

- **RAM**: 32 GB DDR4/DDR5 (64 GB recommended)
  - *Why*: Complex scene rendering and AI model processing require substantial memory

- **Storage**: 1 TB NVMe SSD
  - *Why*: Fast storage essential for loading large simulation assets and models

- **OS**: Ubuntu 22.04 LTS (Native installation recommended)
  - *Note*: While Isaac Sim runs on Windows, ROS 2 (Humble/Iron) is native to Linux. Dual-booting or dedicated Linux machines are mandatory for optimal experience.

#### Recommended Specifications
- **GPU**: NVIDIA RTX 3090 (24GB VRAM) or RTX 4090 (24GB VRAM)
  - *Why*: Allows for smoother "Sim-to-Real" training with complex scenes

- **CPU**: Intel Core i9 (13th Gen+) or AMD Ryzen 9 (7000 series)
  - *Why*: Better multi-core performance for physics calculations

- **RAM**: 64 GB DDR5
  - *Why*: Prevents crashes during complex scene rendering and large model processing

- **Storage**: 2 TB NVMe SSD
  - *Why*: Accommodates multiple simulation environments and datasets

### The "Physical AI" Edge Kit (Required per Student)

Since full humanoid robots are expensive, students learn "Physical AI" by deploying systems to edge computing platforms that mirror production constraints.

#### Core Components
- **The Brain**: NVIDIA Jetson Orin Nano (8GB) or Orin NX (16GB)
  - *Role*: Industry standard for embodied AI
  - *Why*: Students deploy ROS 2 nodes here to understand resource constraints vs. workstations
  - *Performance*: 40 TOPS (trillion operations per second) for AI inference

- **The Eyes (Vision)**: Intel RealSense D435i or D455
  - *Role*: Provides RGB (Color) and Depth (Distance) data
  - *Why*: Essential for VSLAM and Perception modules
  - *Features*: Built-in IMU for additional sensor data

- **The Inner Ear (Balance)**: USB IMU (BNO055)
  - *Note*: Often built into RealSense D435i or Jetson boards, but separate module helps teach IMU calibration

- **Voice Interface**: USB Microphone/Speaker array (e.g., ReSpeaker)
  - *Role*: For "Voice-to-Action" Whisper integration
  - *Requirement*: Far-field microphone for noise cancellation

#### Complete Edge Kit Specifications
| Component | Model | Price (Approx.) | Notes |
|-----------|-------|-----------------|-------|
| The Brain | NVIDIA Jetson Orin Nano Super Dev Kit (8GB) | $249 | New official MSRP, 40 TOPS performance |
| The Eyes | Intel RealSense D435i | $349 | Includes IMU, essential for SLAM |
| The Ears | ReSpeaker USB Mic Array v2.0 | $69 | Far-field microphone for voice commands |
| Power/Misc | High-endurance SD Card (128GB) + cables | $30 | Required for OS and connections |
| **TOTAL** | | **~$700 per kit** | |

## Robot Lab Options

For the "Physical" part of the course, you have three tiers of options depending on budget and learning objectives.

### Option A: The "Proxy" Approach (Recommended for Budget-Conscious Programs)

Use a quadruped (dog) or robotic arm as a proxy. The software principles (ROS 2, VSLAM, Isaac Sim) transfer ~90% effectively to humanoids.

- **Robot**: Unitree Go2 Edu (~$1,800 - $3,000)
  - *Pros*: Highly durable, excellent ROS 2 support, affordable enough for multiple units
  - *Cons*: Not a biped (humanoid)
  - *Best For*: Learning core robotics concepts without humanoid complexity

### Option B: The "Miniature Humanoid" Approach

Small, table-top humanoids for hands-on humanoid experience.

- **Robot**: Unitree G1 (~$16,000) or Robotis OP3 (~$12,000)
  - *Pros*: True bipedal locomotion, educational-focused design
  - *Cons*: Higher cost, more complex control systems
  - *Budget Alternative*: Hiwonder TonyPi Pro (~$600)
    - *Warning*: These kits often run on Raspberry Pi, which cannot run NVIDIA Isaac ROS efficiently

### Option C: The "Premium" Lab (Sim-to-Real Specific)

For actual deployment of capstone projects to real humanoids:

- **Robot**: Unitree G1 Humanoid
  - *Why*: One of the few commercially available humanoids that can walk dynamically
  - *Features*: Open SDK for student ROS 2 controller injection
  - *Investment*: ~$16,000 per unit

## Lab Infrastructure Architecture

To teach this successfully, your lab infrastructure should follow this architecture:

```
Simulation Workstation (RTX-enabled PC)
    ↓ (Trains models, simulates)
Edge Computing Kit (Jetson Orin)
    ↓ (Deploys and runs inference)
Physical Robot (Unitree Go2/G1)
    ↓ (Executes actions in reality)
```

### Component Breakdown
| Component | Hardware | Function |
|-----------|----------|----------|
| Sim Rig | PC with RTX 4080 + Ubuntu 22.04 | Runs Isaac Sim, Gazebo, Unity, trains LLM/VLA models |
| Edge Brain | Jetson Orin Nano | Runs the "Inference" stack, students deploy code here |
| Sensors | RealSense Camera + IMU | Connected to Jetson for real-world data |
| Actuator | Unitree Go2 or G1 (Shared) | Receives motor commands from Jetson |

## Alternative: Cloud-Native "Ether" Lab

If RTX-enabled workstations are not accessible, consider cloud-based alternatives.

### Best For
- Rapid deployment
- Students with weak laptops
- Institutions without high-end hardware budget

### Cloud Workstations (AWS/Azure)
- **Instance Type**: AWS g5.2xlarge (A10G GPU, 24GB VRAM) or g6e.xlarge
- **Software**: NVIDIA Isaac Sim on Omniverse Cloud (requires specific AMI)

#### Cost Calculation Example
- **Instance cost**: ~$1.50/hour (spot/on-demand mix)
- **Usage**: 10 hours/week × 12 weeks = 120 hours
- **Storage** (EBS volumes): ~$25/quarter
- **Total Cloud Bill**: ~$205 per quarter per student

### Local "Bridge" Hardware
You cannot eliminate hardware entirely for "Physical AI":

- **Edge AI Kits**: Still need Jetson Kit for physical deployment (~$700 one-time)
- **Robot**: Still need one physical robot for final demo (~$3,000 Unitree Go2)

### The Latency Challenge
Simulating in the cloud works well, but controlling a real robot from a cloud instance is dangerous due to latency.

**Solution**: Students train in the Cloud, download model weights, and flash to local Jetson kit.

## Hardware Procurement Strategy

### Phased Approach
1. **Phase 1**: Acquire workstations for simulation and development
2. **Phase 2**: Deploy edge kits for AI deployment
3. **Phase 3**: Add physical robots for final demonstrations

### Sharing Models
- **Workstations**: Individual student access required
- **Edge Kits**: Can be shared among 2-3 students for deployment phases
- **Physical Robots**: Shared among teams for final projects

### Maintenance Considerations
- Regular driver updates for GPUs
- Cooling system maintenance for high-performance hardware
- Backup systems for critical components
- Spares for commonly failing components

## Troubleshooting Common Hardware Issues

### GPU-Related Issues
- **Isaac Sim crashes**: Check VRAM usage and upgrade if necessary
- **Slow simulation**: Verify RT cores and CUDA compatibility
- **Driver conflicts**: Use NVIDIA's official drivers, avoid distribution packages

### Network and Connectivity
- **ROS 2 communication**: Ensure proper network configuration between devices
- **Camera feed issues**: Check USB bandwidth and connection stability
- **Latency problems**: Minimize network hops between components

## Fun Facts

:::info{.fun-fact}
**Hardware Evolution**: The computational requirements for robotics have increased dramatically over the past decade. What required a supercomputer in 2010 can now run on a high-end gaming laptop, making advanced robotics education accessible to more institutions.
:::

:::info{.fun-fact}
**Jetson Power**: The NVIDIA Jetson Orin Nano can deliver 40 TOPS of AI performance while consuming only 15-25 watts—making it 10x more power-efficient than a desktop GPU for AI inference tasks.
:::

## Budget Planning

### Per-Student Investment
- **Minimum Setup**: $1,000 (Edge kit + cloud access)
- **Recommended Setup**: $3,000 (Workstation + Edge kit + shared robot)
- **Premium Setup**: $20,000+ (Complete workstation + robot access)

### Institutional Considerations
- **Shared Resources**: Workstations can be shared during off-peak hours
- **Phased Deployment**: Start with cloud solution, transition to on-premise
- **Grant Opportunities**: Many funding agencies support robotics education infrastructure

## Next Steps

Once you have the appropriate hardware configured:
1. Install Ubuntu 22.04 LTS on workstations
2. Set up ROS 2 Humble Hawksbill
3. Configure NVIDIA drivers and CUDA
4. Install Isaac Sim and required dependencies
5. Test basic functionality before course start
6. Prepare backup plans for hardware failures

The hardware investment enables students to work with industry-standard tools and prepares them for careers in robotics and AI development.