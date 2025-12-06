# Implementation Plan: Dual Platform Setup (Docusaurus + Next.js)

**Branch**: `003-dual-platform-setup` | **Date**: 2025-12-06 | **Spec**: [specs/003-dual-platform-setup/spec.md](spec.md)
**Input**: Feature specification from `/specs/[003-dual-platform-setup]/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Implementation of a dual-platform approach for the Physical AI & Humanoid Robotics Textbook Platform, supporting both Docusaurus (for GitHub Pages deployment) and Next.js (for modern hosting platforms) to maximize accessibility and feature richness. This approach ensures the textbook content and interactive features (RAG chatbot, personalization, translation) work consistently across both platforms while providing deployment flexibility.

## Technical Context

**Language/Version**: TypeScript/JavaScript for frontend, Python 3.11+ for backend services
**Primary Dependencies**: Docusaurus 3.x, Next.js 14+ with App Router, FastAPI, OpenAI SDK, Qdrant, PostgreSQL
**Storage**: PostgreSQL for user data and preferences, Qdrant for RAG vector storage, file system for textbook content
**Testing**: pytest for backend, Jest for frontend, Playwright for E2E tests
**Target Platform**: Web application with dual deployment options (GitHub Pages + Modern Hosting)
**Project Type**: web - determines source structure
**Performance Goals**: Support 1000+ concurrent users, RAG responses under 3 seconds, consistent performance across both platforms
**Constraints**: <200ms p95 for content delivery, <1GB memory for RAG operations, mobile-responsive design
**Scale/Scope**: Support 10k+ registered users, 50+ textbook chapters, 1000+ fun fact cards

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- **I. Spec-Driven Book Creation**: Implementation follows the spec-driven approach outlined in the feature specification
- **II. AI-Native & Agent-Assisted Development**: RAG chatbot leverages Claude Code and OpenAI Agent SDK as specified, with Claude Code for development assistance
- **III. Interactive Learning Experience**: Core requirement for RAG chatbot and personalization features met across both platforms
- **IV. Robust Technical Content**: System supports technically accurate content delivery with proper formatting in both platforms
- **V. Deployment and Accessibility**: Architecture supports dual deployment (GitHub Pages with Docusaurus + Modern hosting with Next.js) as outlined in constitution
- **VI. Hardware and Simulation Awareness**: Platform accommodates content for hardware requirements as outlined in constitution

## Project Structure

### Documentation (this feature)
```text
specs/003-dual-platform-setup/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)
```text
.
├── backend/                 # Shared backend services for both platforms
│   ├── src/
│   │   ├── models/
│   │   │   ├── user.py
│   │   │   ├── textbook_content.py
│   │   │   ├── personalization.py
│   │   │   ├── translation.py
│   │   │   └── theme_preference.py
│   │   ├── services/
│   │   │   ├── auth_service.py
│   │   │   ├── rag_service.py
│   │   │   ├── personalization_service.py
│   │   │   ├── translation_service.py
│   │   │   └── theme_service.py
│   │   ├── api/
│   │   │   ├── auth_api.py
│   │   │   ├── rag_api.py
│   │   │   ├── content_api.py
│   │   │   └── user_preferences_api.py
│   │   └── main.py
│   └── tests/
│       ├── unit/
│       ├── integration/
│       └── contract/
├── frontend/                # Next.js implementation with App Router
│   ├── src/
│   │   ├── app/
│   │   │   ├── layout.tsx
│   │   │   ├── page.tsx
│   │   │   ├── login/
│   │   │   ├── register/
│   │   │   ├── chat/
│   │   │   ├── book/
│   │   │   └── textbook-content/
│   │   │       └── [slug]/
│   │   │           └── page.tsx
│   │   ├── components/
│   │   │   ├── Auth/
│   │   │   ├── RAGChatbot/
│   │   │   ├── Personalization/
│   │   │   ├── Translation/
│   │   │   ├── FunFactCard/
│   │   │   └── ThemeToggle/
│   │   ├── services/
│   │   └── utils/
│   ├── public/
│   └── tests/
├── docs-platform/           # Docusaurus implementation for GitHub Pages
│   ├── docs/
│   │   ├── textbook/
│   │   │   ├── introduction-to-physical-ai.md
│   │   │   ├── ros2-the-robotic-nervous-system.md
│   │   │   ├── digital-twin-simulation.md
│   │   │   ├── nvidia-isaac-ai-brain.md
│   │   │   ├── vision-language-action-integration.md
│   │   │   ├── hardware-requirements-and-setup.md
│   │   │   ├── personalization-and-user-experience.md
│   │   │   ├── multilingual-support-and-translation.md
│   │   │   ├── fun-fact-cards-and-engagement.md
│   │   │   ├── theming-and-customization.md
│   │   │   ├── deployment-and-operations.md
│   │   │   └── conclusion-and-future-directions.md
│   │   ├── quizzes/
│   │   │   ├── introduction-to-physical-ai-quiz.md
│   │   │   ├── ros2-the-robotic-nervous-system-quiz.md
│   │   │   ├── ...
│   │   │   └── conclusion-and-future-directions-quiz.md
│   │   └── intro.md
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   └── css/
│   ├── static/
│   └── tests/
├── shared/                  # Shared content and utilities
│   ├── content/
│   │   ├── textbook/
│   │   └── quizzes/
│   └── utils/
└── docker-compose.yml       # Multi-platform orchestration
```

**Structure Decision**: Selected Option 2: Web application structure to separate frontend (Next.js and Docusaurus implementations) from backend services (authentication, RAG, personalization, translation). This allows both frontend platforms to be deployed independently while sharing the same backend services, maximizing accessibility and feature consistency.

## Phase 2: Implementation Planning Complete

**Status**: Tasks file generated successfully at `/specs/003-dual-platform-setup/tasks.md`
**Task Count**: 107 implementation tasks across all user stories
**Next Step**: Execute implementation following the generated tasks

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| Dual Platform Architecture | Required for maximum accessibility (GitHub Pages + Modern Hosting) | Single platform would limit deployment options and accessibility |
| Shared Backend Services | Required for user session and data consistency across platforms | Separate backends would create data inconsistency and maintenance overhead |
| Synchronized Content | Required for consistent learning experience across platforms | Platform-specific content would confuse users switching between platforms |
