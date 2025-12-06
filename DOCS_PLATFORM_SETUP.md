# Physical AI & Humanoid Robotics Textbook Platform - Dual Platform Setup

## Overview

This project implements a dual-platform approach for the Physical AI & Humanoid Robotics Textbook Platform to maximize accessibility and reach:

1. **Next.js Version** (in `frontend/`): Modern, feature-rich version deployed to Vercel/Netlify with advanced functionality
2. **Docusaurus Version** (in `docs-platform/`): Lightweight version deployed to GitHub Pages for maximum accessibility

Both platforms share the same backend services and content repository to ensure consistency.

## Architecture

```
hackathon/
├── backend/                 # Shared backend services (auth, RAG, personalization, etc.)
├── frontend/                # Next.js implementation with App Router
├── docs-platform/           # Docusaurus implementation for GitHub Pages
├── shared-content/          # Shared textbook content and materials
└── docker-compose.yml       # Multi-platform orchestration
```

## Shared Backend Services

Both platforms connect to the same backend services located in the `backend/` directory:

- **Authentication API**: User registration, login, and session management
- **RAG Service**: AI-powered chatbot with textbook content knowledge base
- **Personalization Service**: Content adaptation based on user background
- **Translation Service**: Urdu translation functionality
- **User Preferences API**: Theme, settings, and preference management

## Content Synchronization

Textbook content is maintained in a shared format that can be consumed by both platforms:

- Content is authored in Markdown/MDX format
- Both platforms use the same content repository
- Updates to content automatically propagate to both platforms

## Deployment Strategies

### Next.js Platform (Advanced Features)
- **Hosting**: Vercel, Netlify, or other modern hosting platforms
- **Features**: Full functionality including advanced RAG, personalization, and interactive elements
- **Best for**: Users wanting the richest experience with all features

### Docusaurus Platform (Maximum Accessibility)
- **Hosting**: GitHub Pages
- **Features**: Core textbook content with essential interactive features
- **Best for**: Users wanting guaranteed access via GitHub Pages

## Development Workflow

### Working with Both Platforms

1. **Content Updates**: Update content in the shared content repository
2. **Backend Changes**: Modify backend services in the `backend/` directory (affects both platforms)
3. **Frontend Changes**:
   - Next.js-specific features go in `frontend/`
   - Docusaurus-specific features go in `docs-platform/`
4. **Testing**: Test functionality on both platforms to ensure consistency

### Running Locally

To run both platforms simultaneously:

```bash
# Terminal 1: Run the backend
cd backend
python -m uvicorn src.main:app --reload --port 8000

# Terminal 2: Run the Next.js frontend
cd frontend
npm run dev

# Terminal 3: Run the Docusaurus frontend
cd docs-platform
npm start
```

Both frontends will connect to the same backend API.

## Feature Parity

Both platforms implement the same core features:

| Feature | Next.js Version | Docusaurus Version | Notes |
|---------|----------------|--------------------|-------|
| Textbook Content | ✅ | ✅ | Same content, different presentation |
| User Authentication | ✅ | ✅ | Shared backend authentication |
| RAG Chatbot | ✅ | ✅ | Same knowledge base, different UI |
| Personalization | ✅ | ✅ | Same user profiles, different UI |
| Urdu Translation | ✅ | ✅ | Shared translation service |
| Theme Support | ✅ | ✅ | Light/dark/system themes |
| Fun Fact Cards | ✅ | ✅ | Same content, different presentation |

## API Integration

Both platforms connect to the same backend API endpoints:

- Authentication: `http://localhost:8000/auth/*`
- Content: `http://localhost:8000/content/*`
- RAG: `http://localhost:8000/rag/*`
- User Preferences: `http://localhost:8000/preferences/*`

## Maintenance Guidelines

1. **Backend Changes**: Affect both platforms - test on both after changes
2. **Content Updates**: Automatically apply to both platforms
3. **UI/UX Changes**: Need to be implemented separately on each platform
4. **Bug Fixes**: Check both platforms for the same issue

## Environment Configuration

### Next.js Platform
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### Docusaurus Platform
```env
API_BASE_URL=http://localhost:8000
```

## Deployment Commands

### Next.js Platform
```bash
# Build and deploy to Vercel/Netlify
cd frontend
npm run build
```

### Docusaurus Platform
```bash
# Build and deploy to GitHub Pages
cd docs-platform
npm run build
# Then deploy the build/ directory to GitHub Pages
```

## Quality Assurance

- Both platforms must pass the same functional tests
- Content consistency is verified through automated checks
- Performance metrics are tracked for both platforms
- User feedback is aggregated from both platforms