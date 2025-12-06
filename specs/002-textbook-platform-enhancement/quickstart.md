# Quickstart Guide: Physical AI & Humanoid Robotics Textbook Platform

**Feature**: 002-textbook-platform-enhancement
**Date**: 2025-12-05

## Overview

This guide provides instructions to quickly set up and run the Physical AI & Humanoid Robotics Textbook Platform with authentication, RAG chatbot, personalization, translation, and theme support.

## Prerequisites

- Node.js 18+ (for frontend/Docusaurus)
- Python 3.11+ (for backend/FastAPI)
- PostgreSQL 12+ (for user data)
- Qdrant (for RAG vector storage)
- OpenAI API key
- Git

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
# Edit .env with your database credentials and API keys
```

### 3. Frontend Setup

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Set up environment variables
cp .env.example .env
# Edit .env with your backend API URL and other configurations
```

### 4. Database Setup

```bash
# With backend virtual environment activated
cd backend

# Run database migrations
python -m alembic upgrade head
```

### 5. Vector Database Setup (Qdrant)

```bash
# Make sure Qdrant is running (can be run with Docker)
docker run -d --name qdrant -p 6333:6333 qdrant/qdrant

# Initialize RAG indexes
cd backend
python -m scripts/init_rag_db.py
```

### 6. Environment Variables

Create `.env` files in both backend and frontend with the following variables:

**Backend (.env):**
```
DATABASE_URL=postgresql://username:password@localhost:5432/textbook_platform
OPENAI_API_KEY=your_openai_api_key
QDRANT_URL=http://localhost:6333
SECRET_KEY=your_secret_key_for_auth
```

**Frontend (.env):**
```
REACT_APP_API_URL=http://localhost:8000
REACT_APP_OPENAI_API_KEY=your_openai_api_key
```

## Running the Application

### Development Mode

**Backend:**
```bash
cd backend
source venv/bin/activate  # Activate virtual environment
uvicorn src.main:app --reload --port 8000
```

**Frontend:**
```bash
cd frontend
npm start
```

### Production Mode

**Backend:**
```bash
cd backend
gunicorn src.main:app:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

**Frontend:**
```bash
cd frontend
npm run build
# Serve the build directory with your preferred web server
```

## Key Features Setup

### Authentication
- User registration and login endpoints available at `/auth/register` and `/auth/login`
- Session management handled automatically
- Better-auth integration provides secure authentication

### RAG Chatbot
- Available at `/api/rag/chat` endpoint
- Requires authentication to use
- Connects to textbook content for context-aware responses

### Content Personalization
- User background collected during registration
- Content adapts based on user's software/hardware experience
- Preferences stored in personalization profiles

### Urdu Translation
- Translation available via `/api/translation/urdu` endpoint
- Single button translation for chapters
- Cached translations for performance

### Theme Support
- Light/dark/system themes available
- User preferences stored in browser/local storage
- CSS variables used for theme switching

## API Endpoints

### Authentication
- `POST /auth/register` - User registration
- `POST /auth/login` - User login
- `POST /auth/logout` - User logout
- `GET /auth/me` - Get current user info

### Content
- `GET /content` - List textbook content
- `GET /content/{slug}` - Get specific content
- `GET /content/{slug}/personalize` - Get personalized content
- `GET /content/{slug}/translate/ur` - Get Urdu translation

### RAG Chatbot
- `POST /rag/chat` - Chat with RAG system
- `POST /rag/validate` - Validate question relevance

### User Preferences
- `GET /preferences/theme` - Get user theme preference
- `PUT /preferences/theme` - Update user theme preference
- `GET /preferences/personalization` - Get personalization profile
- `PUT /preferences/personalization` - Update personalization profile

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

## Deployment

### Frontend to GitHub Pages
```bash
cd frontend
npm run build
# Deploy the build directory to GitHub Pages
```

### Backend
Deploy the backend service to your preferred cloud platform (AWS, GCP, Azure, etc.) with the required dependencies and environment variables.