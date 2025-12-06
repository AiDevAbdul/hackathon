# Physical AI & Humanoid Robotics Textbook Platform

A comprehensive educational platform for learning Physical AI and Humanoid Robotics with AI-powered assistance, personalization, and multilingual support.

## Overview

The Physical AI & Humanoid Robotics Textbook Platform is an innovative educational system that combines traditional textbook learning with modern AI technologies. The platform features:

- **Interactive Learning**: AI-powered RAG (Retrieval-Augmented Generation) chatbot for immediate Q&A
- **Personalization**: Content adapted to user's software and hardware background
- **Multilingual Support**: Urdu translation with single-button language switching
- **Modern Pedagogy**: Fun fact cards and engagement elements throughout
- **Accessibility**: Light/dark/system themes with WCAG-compliant design
- **Dual Deployment**: Available on both GitHub Pages (Docusaurus) and modern hosting (Next.js)

## Features

### 1. AI-Powered Learning Assistant
- Context-aware responses based on textbook content
- Source attribution for all answers
- Real-time interaction with learning material

### 2. Personalized Content
- Adapts to user's technical background (software/hardware focus)
- Customized examples and complexity levels
- Learning path recommendations

### 3. Multilingual Access
- Urdu translation for broader accessibility
- AI-powered translation with quality validation
- Single-click language switching

### 4. Engaging Pedagogy
- Fun fact cards throughout content
- Interactive elements to maintain engagement
- Modern learning approaches

### 5. Theme Support
- Light, dark, and system-default themes
- High contrast mode for accessibility
- Focus and comfort modes for different needs

## Architecture

### Dual-Platform Approach
The platform is implemented with dual compatibility:

1. **Next.js Frontend**: Modern, feature-rich version with advanced capabilities
   - App Router architecture
   - Server-side rendering and static generation
   - Advanced interactivity and performance

2. **Docusaurus Frontend**: Lightweight version for GitHub Pages accessibility
   - Static site generation
   - Optimized for documentation-style content
   - Maximum accessibility and reach

### Backend Services
- **Authentication**: JWT-based user management with background collection
- **RAG System**: OpenAI-powered chatbot with Qdrant vector database
- **Personalization**: Content adaptation based on user profile
- **Translation**: AI-powered content translation with caching
- **Progress Tracking**: User learning progress and preferences

## Technology Stack

- **Frontend (Next.js)**: React with App Router, TypeScript, Tailwind CSS
- **Frontend (Docusaurus)**: Docusaurus for GitHub Pages deployment
- **Backend**: FastAPI with Python 3.11+
- **Database**: PostgreSQL for user data and content
- **Vector Database**: Qdrant for RAG functionality
- **Caching**: Redis for performance optimization
- **AI Integration**: OpenAI API for RAG and translation
- **Containerization**: Docker and Docker Compose

## Project Structure

```
hackathon/
├── backend/                 # Shared backend services
│   ├── src/
│   │   ├── models/          # Database models
│   │   ├── services/        # Business logic services
│   │   ├── api/             # API endpoints
│   │   └── middleware/      # Authentication and other middleware
│   └── tests/
├── frontend/                # Next.js frontend implementation
│   ├── src/
│   │   ├── app/             # App Router pages
│   │   ├── components/      # Reusable components
│   │   ├── services/        # Client-side services
│   │   └── utils/           # Utility functions
│   └── tests/
├── docs-platform/           # Docusaurus frontend for GitHub Pages
│   ├── docs/                # Textbook content
│   ├── src/                 # Custom components
│   └── tests/
├── specs/                   # Feature specifications
│   ├── 002-textbook-platform-enhancement/
│   └── 003-dual-platform-setup/
├── docker-compose.yml       # Container orchestration
└── README.md               # This file
```

## Getting Started

### Prerequisites

- Node.js 18+ (for frontend development)
- Python 3.11+ (for backend services)
- Docker and Docker Compose
- OpenAI API Key
- PostgreSQL (or Docker for containerized database)

### Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd <repository-name>
   ```

2. Set up backend:
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. Set up frontend (Next.js):
   ```bash
   cd frontend
   npm install
   ```

4. Set up frontend (Docusaurus):
   ```bash
   cd docs-platform
   npm install
   ```

5. Configure environment variables:
   - Copy `.env.example` to `.env` in both backend and frontend directories
   - Set your OpenAI API key and database credentials

6. Start the services:
   ```bash
   # Using Docker Compose
   docker-compose up -d

   # Or start services individually
   # Backend: uvicorn src.main:app --reload --port 8000
   # Next.js frontend: npm run dev
   # Docusaurus frontend: npm start
   ```

## API Endpoints

### Authentication
- `POST /auth/register` - User registration
- `POST /auth/login` - User login
- `GET /auth/me` - Get current user

### Content
- `GET /content` - Get textbook content list
- `GET /content/{slug}` - Get specific content
- `GET /content/{slug}/personalize` - Get personalized content
- `GET /content/{slug}/translate/ur` - Get Urdu translation

### RAG Chatbot
- `POST /rag/chat` - Chat with the RAG system
- `POST /rag/validate` - Validate question relevance

### User Preferences
- `GET /preferences/theme` - Get theme preference
- `POST /preferences/theme` - Set theme preference
- `GET /preferences/personalization` - Get personalization profile
- `POST /preferences/personalization` - Set personalization profile

## Development

### Running in Development Mode

1. Start backend:
   ```bash
   cd backend
   uvicorn src.main:app --reload --port 8000
   ```

2. Start Next.js frontend:
   ```bash
   cd frontend
   npm run dev
   ```

3. Start Docusaurus frontend:
   ```bash
   cd docs-platform
   npm start
   ```

### Running Tests

Backend tests:
```bash
cd backend
python -m pytest
```

Frontend tests:
```bash
cd frontend
npm test
```

Docusaurus tests:
```bash
cd docs-platform
npm test
```

## Deployment

### Next.js Deployment
The Next.js frontend can be deployed to:
- Vercel (recommended)
- Netlify
- Any Node.js hosting platform

### Docusaurus Deployment
The Docusaurus frontend can be deployed to:
- GitHub Pages
- Netlify
- Any static hosting platform

### Backend Deployment
The backend services can be deployed as Docker containers to:
- AWS ECS
- Google Cloud Run
- Azure Container Instances
- Any containerized hosting platform

## Contributing

We welcome contributions to the Physical AI & Humanoid Robotics Textbook Platform! Please see our [contributing guidelines](docs/contributing.md) for more information.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Thanks to the Physical AI & Humanoid Robotics course team for inspiration
- Built with Claude Code for AI-assisted development
- Special thanks to the open-source community for the amazing tools and libraries

## Contact

For questions or support, please open an issue in the repository or contact the development team.