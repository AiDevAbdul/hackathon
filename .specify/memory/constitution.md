<!--
Sync Impact Report:
Version change: 1.2.0 → 1.3.0
Modified principles:
  - PRINCIPLE_5_NAME: V. Deployment and Accessibility (changed to dual-platform approach: Docusaurus + Next.js)
  - SECTION_2_NAME: Development Workflow (updated to reflect dual-platform implementation)
  - SECTION_3_NAME: Quality Gates (updated to reflect dual-platform testing and optimization)
Added sections: None
Removed sections: None
Templates requiring updates:
  - .specify/templates/plan-template.md: ⚠ pending
  - .specify/templates/spec-template.md: ⚠ pending
  - .specify/templates/tasks-template.md: ⚠ pending
  - .specify/templates/commands/sp.constitution.md: ✅ updated
  - README.md: ⚠ pending
  - docs/quickstart.md: ⚠ pending
Follow-up TODOs: Update templates to reflect dual-platform approach
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
The textbook will be maintained in dual formats: a Docusaurus-based version for GitHub Pages deployment and a Next.js App Router version for modern hosting platforms (Vercel, Netlify, etc.), ensuring maximum accessibility. Both versions must have fully functional RAG chatbot and interactive features.

### VI. Hardware and Simulation Awareness
Acknowledge and address the significant hardware requirements for Physical AI, including high-performance workstations for simulation and edge computing kits for physical deployment. Course content should guide students through both on-premise and cloud-native lab setups.

## Development Workflow

- **Spec Creation:** Book structure and content modules are defined in `spec.md` using Spec-Kit Plus.
- **Content Generation:** AI agents assist in drafting, refining, and verifying textbook content.
- **Feature Implementation:** RAG chatbot, personalization, and translation features are integrated into both Docusaurus and Next.js projects to maintain dual-platform compatibility.
- **Deployment:** The book is deployed to GitHub Pages (Docusaurus version) and various hosting platforms (Next.js version) to maximize reach and accessibility.
- **Continuous Improvement:** Feedback from the RAG chatbot and user interactions will inform content updates and feature enhancements across both platforms.

## Quality Gates

- **Technical Accuracy:** All technical content in the book is rigorously reviewed for accuracy.
- **Functionality Testing:** The RAG chatbot and interactive features are thoroughly tested for correctness and responsiveness on both Docusaurus and Next.js platforms.
- **Accessibility Review:** Ensure both published versions (Docusaurus and Next.js) are accessible and function correctly across various devices and browsers.
- **Performance Optimization:** Both Docusaurus and Next.js sites and embedded features are optimized for loading speed and responsiveness.
- **User Feedback Integration:** Mechanisms for collecting and incorporating user feedback are established for both platforms.

## Governance

- This Constitution outlines the foundational principles for the Physical AI & Humanoid Robotics Textbook Project.
- All project deliverables and contributions must align with these principles and the hackathon requirements.
- Amendments to these principles require explicit agreement from the project leads.
- Regular reviews will be conducted to ensure ongoing compliance with technical accuracy and user experience standards.
- Refer to the project documentation for specific requirements, timelines, and bonus point opportunities.

**Version**: 1.3.0 | **Ratified**: 2025-12-05 | **Last Amended**: 2025-12-06