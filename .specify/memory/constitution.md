<!--
Sync Impact Report:
Version change: 1.0.0 → 1.1.0
Modified principles:
  - PROJECT_NAME: Physical AI & Humanoid Robotics Textbook Project
  - PRINCIPLE_1_NAME: I. Spec-Driven Book Creation
  - PRINCIPLE_2_NAME: II. AI-Native & Agent-Assisted Development
  - PRINCIPLE_3_NAME: III. Interactive Learning Experience
  - PRINCIPLE_4_NAME: IV. Robust Technical Content
  - PRINCIPLE_5_NAME: V. Deployment and Accessibility
  - PRINCIPLE_6_NAME: VI. Hardware and Simulation Awareness
  - SECTION_2_NAME: Development Workflow
  - SECTION_3_NAME: Quality Gates
  - GOVERNANCE_RULES: Project Governance
Added sections: None
Removed sections: None
Templates requiring updates:
  - .specify/templates/plan-template.md: ✅ updated
  - .specify/templates/spec-template.md: ✅ updated
  - .specify/templates/tasks-template.md: ✅ updated
  - .specify/templates/commands/sp.constitution.md: ✅ updated
  - README.md: ⚠ pending
  - docs/quickstart.md: ⚠ pending
Follow-up TODOs: None
-->

# Physical AI & Humanoid Robotics Textbook Project Constitution

## Core Principles

### I. Spec-Driven Book Creation
The textbook content and structure are defined through a spec-driven approach using Spec-Kit Plus. All book elements (chapters, modules, exercises) must be clearly outlined in specifications before implementation.

### II. AI-Native & Agent-Assisted Development
Leverage Claude Code and AI agents for content generation, RAG chatbot development, and other development tasks. Prioritize reusable intelligence through Claude Code Subagents and Agent Skills to enhance efficiency and capabilities.

### III. Interactive Learning Experience
The textbook must include an integrated RAG chatbot for interactive Q&A. Personalization and translation features should be implemented to cater to diverse learning needs and improve user engagement.

### IV. Robust Technical Content
Content for the Physical AI & Humanoid Robotics course must be technically accurate, detailed, and cover ROS 2, Gazebo, Unity, NVIDIA Isaac, and Vision-Language-Action (VLA) models as outlined in the course details.

### V. Deployment and Accessibility
The textbook will be deployed using Docusaurus to GitHub Pages, ensuring public accessibility. The RAG chatbot and other interactive features must be fully functional within the published book.

### VI. Hardware and Simulation Awareness
Acknowledge and address the significant hardware requirements for Physical AI, including high-performance workstations for simulation and edge computing kits for physical deployment. Course content should guide students through both on-premise and cloud-native lab setups.

## Development Workflow

- **Spec Creation:** Book structure and content modules are defined in `spec.md` using Spec-Kit Plus.
- **Content Generation:** AI agents assist in drafting, refining, and verifying textbook content.
- **Feature Implementation:** RAG chatbot, personalization, and translation features are integrated into the Docusaurus project.
- **Deployment:** The book is deployed to GitHub Pages.
- **Continuous Improvement:** Feedback from the RAG chatbot and user interactions will inform content updates and feature enhancements.

## Quality Gates

- **Technical Accuracy:** All technical content in the book is rigorously reviewed for accuracy.
- **Functionality Testing:** The RAG chatbot and interactive features are thoroughly tested for correctness and responsiveness.
- **Accessibility Review:** Ensure the published book is accessible and functions correctly across various devices and browsers.
- **Performance Optimization:** The Docusaurus site and embedded features are optimized for loading speed and responsiveness.
- **User Feedback Integration:** Mechanisms for collecting and incorporating user feedback are established.

## Governance

- This Constitution outlines the foundational principles for the Physical AI & Humanoid Robotics Textbook Project.
- All project deliverables and contributions must align with these principles and the hackathon requirements.
- Amendments to these principles require explicit agreement from the project leads.
- Regular reviews will be conducted to ensure ongoing compliance with technical accuracy and user experience standards.
- Refer to the project documentation for specific requirements, timelines, and bonus point opportunities.

**Version**: 1.1.0 | **Ratified**: 2025-12-05 | **Last Amended**: 2025-12-05