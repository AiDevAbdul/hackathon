---
description: "Quickstart guide for dual-platform setup (Docusaurus + Next.js)"
---

# Quickstart: Physical AI & Humanoid Robotics Textbook Platform

**Feature**: 003-dual-platform-setup
**Date**: 2025-12-06
**Status**: Ready for Implementation
**Input**: Feature specification from `/specs/[003-dual-platform-setup]/spec.md`

## Overview

This quickstart guide provides instructions to quickly set up and run the Physical AI & Humanoid Robotics Textbook Platform with dual-platform support (Docusaurus for GitHub Pages and Next.js for modern hosting). The platform includes authentication, RAG chatbot, personalization, translation, and modern pedagogical features.

## Prerequisites

- **Node.js**: 18+ (for frontend development)
- **Python**: 3.11+ (for backend services)
- **Docker**: 20+ (for containerized deployment)
- **Docker Compose**: Latest version
- **OpenAI API Key**: For RAG functionality
- **Git**: For version control
- **PNPM**: For package management (recommended)

## Setup Instructions

### 1. Clone the Repository

```bash
git clone <repository-url>
cd <repository-name>
```

### 2. Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your database credentials, API keys, and configuration
```

### 3. Frontend Setup (Next.js)

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
pnpm install  # or npm install

# Set up environment variables
cp .env.example .env
# Edit .env with your backend API URL and other configurations
```

### 4. Frontend Setup (Docusaurus)

```bash
# Navigate to docs-platform directory
cd docs-platform

# Install dependencies
pnpm install  # or npm install

# Set up environment variables
cp .env.example .env
# Edit .env with your backend API URL and other configurations
```

### 5. Database Setup

```bash
# With backend virtual environment activated
cd backend

# Run database migrations
python -m alembic upgrade head
```

### 6. Vector Database Setup (Qdrant)

```bash
# Start Qdrant container
docker run -d --name qdrant -p 6333:6333 -v $(pwd)/qdrant_data:/qdrant/storage qdrant/qdrant

# Initialize RAG indexes (run from backend directory)
cd backend
python -m scripts/init_rag_db.py
```

### 7. Environment Configuration

Create `.env` files in both backend and frontend directories with the following variables:

**Backend (.env)**:
```env
DATABASE_URL=postgresql://user:password@localhost:5432/textbook_platform
OPENAI_API_KEY=your_openai_api_key
QDRANT_URL=http://localhost:6333
SECRET_KEY=your_very_long_secret_key_for_jwt_tokens
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
DEBUG=True
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:3001,http://localhost:5173
```

**Frontend (.env)**:
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_WEBSITE_URL=http://localhost:3000
NODE_ENV=development
```

**Docusaurus (.env)**:
```env
API_BASE_URL=http://localhost:8000
REACT_APP_API_URL=http://localhost:8000
```

## Running the Application

### Development Mode

**Backend**:
```bash
cd backend
source venv/bin/activate  # Activate virtual environment
uvicorn src.main:app --reload --port 8000
```

**Next.js Frontend**:
```bash
cd frontend
npm run dev
# Access at http://localhost:3000
```

**Docusaurus Frontend**:
```bash
cd docs-platform
npm run start
# Access at http://localhost:3001
```

### Production Mode

**Backend**:
```bash
cd backend
gunicorn src.main:app:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

**Next.js Frontend**:
```bash
cd frontend
npm run build
npm start
# Serves on http://localhost:3000
```

**Docusaurus Frontend**:
```bash
cd docs-platform
npm run build
npm run serve
# Serves on http://localhost:3001
```

## Containerized Deployment

### Using Docker Compose

```bash
# From the project root directory
docker-compose -f docker-compose.prod.yml up -d

# Verify services are running
docker-compose -f docker-compose.prod.yml ps

# Run database migrations
docker-compose -f docker-compose.prod.yml exec backend python -m alembic upgrade head
```

## Key Features Setup

### Authentication
- User registration and login available at `/auth/register` and `/auth/login`
- Session management with JWT tokens
- Better-auth integration for secure authentication

### RAG Chatbot
- Available at `/api/rag/chat` endpoint
- Requires authentication to use
- Connects to textbook content for context-aware responses
- Try asking: "Explain ROS 2 architecture for humanoid robots"

### Content Personalization
- User background collected during registration
- Content adapts based on software/hardware experience
- Preferences stored in personalization profiles

### Urdu Translation
- Translation available via `/api/content/translate/ur` endpoint
- Single button translation for chapters
- Cached translations for performance

### Fun Fact Cards
- Engaging supplementary content in each chapter
- Different positioning options (inline, sidebar, popup)
- Modern pedagogical approach to enhance learning

### Theme Support
- Light, dark, and system theme options
- User preference persistence across sessions
- CSS variables for consistent styling

## API Endpoints

### Authentication (`/auth`)
- `POST /auth/register`: User registration
- `POST /auth/login`: User login
- `GET /auth/me`: Get current user info
- `POST /auth/logout`: Logout user

### Content (`/content`)
- `GET /content`: Get list of textbook content
- `GET /content/{slug}`: Get specific content by slug
- `GET /content/{slug}/personalize`: Get personalized content
- `GET /content/{slug}/translate/ur`: Get Urdu translation
- `GET /content/{slug}/fun-facts`: Get fun fact cards for content

### RAG Chatbot (`/rag`)
- `POST /rag/chat`: Chat with RAG system
- `POST /rag/validate`: Validate question relevance

### User Preferences (`/preferences`)
- `GET /preferences/theme`: Get user's theme preference
- `POST /preferences/theme`: Set user's theme preference
- `GET /preferences/personalization`: Get user's personalization profile
- `POST /preferences/personalization`: Set user's personalization profile

### Admin (`/admin`)
- `GET /admin/fun-facts`: Get all fun fact cards (admin only)
- `POST /admin/fun-facts`: Create new fun fact card (admin only)

## Testing

### Backend Tests
```bash
cd backend
python -m pytest
```

### Frontend Tests
```bash
cd frontend
npm test
```

### Docusaurus Tests
```bash
cd docs-platform
npm test
```

## Deployment Options

### Next.js Deployment
- **Vercel**: `npm run build && vercel deploy`
- **Netlify**: `npm run build && netlify deploy`
- **Custom Server**: Deploy the `frontend/build` directory

### Docusaurus Deployment
- **GitHub Pages**: `npm run build && npm run deploy`
- **Netlify**: Upload `docs-platform/build` directory
- **Custom Server**: Serve the static files from `docs-platform/build`

## Troubleshooting

### Common Issues

#### Backend Not Starting
- **Issue**: Backend service won't start
- **Solution**: Check that PostgreSQL and Qdrant are running
- **Command**: `docker-compose up db qdrant` to start required services

#### API Requests Failing
- **Issue**: Frontend can't connect to backend APIs
- **Solution**: Verify BACKEND_URL in frontend environment variables
- **Check**: Make sure backend is running on specified port

#### RAG Chatbot Not Responding
- **Issue**: Chatbot returns errors or no response
- **Solution**: Check OpenAI API key and Qdrant connection
- **Verify**: Ensure content has been indexed in the vector database

#### Authentication Issues
- **Issue**: Login/register not working
- **Solution**: Verify database connection and JWT secret key
- **Check**: Ensure CORS settings allow frontend domain

### Getting Help
- Check the logs: `docker-compose logs <service-name>`
- Verify environment variables are set correctly
- Ensure all required services are running
- Consult the full documentation in `/docs/` directory

## Next Steps

1. **Customize Content**: Add your own textbook content to the platform
2. **Extend Functionality**: Add new features to the existing architecture
3. **Optimize Performance**: Implement caching and optimization strategies
4. **Enhance Security**: Add additional security measures for production
5. **Scale Deployment**: Configure load balancing and clustering for high traffic