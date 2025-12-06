# Physical AI & Humanoid Robotics Textbook Platform - API Documentation

## Overview

This document provides comprehensive documentation for the Physical AI & Humanoid Robotics Textbook Platform API. The API provides endpoints for authentication, content management, RAG chatbot, personalization, translation, and theme management.

## Base URL

```
http://localhost:8000
```

## Authentication

Most endpoints require authentication using JWT tokens. Include the token in the Authorization header:

```
Authorization: Bearer <your-jwt-token>
```

## API Endpoints

### Authentication (`/auth`)

#### POST `/auth/register`
Register a new user.

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "securepassword",
  "name": "John Doe",
  "background_software": "Software Engineer",
  "background_hardware": "Robotics Enthusiast"
}
```

**Response:**
```json
{
  "access_token": "jwt-token",
  "token_type": "bearer"
}
```

#### POST `/auth/login`
Login with existing credentials.

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "securepassword"
}
```

**Response:**
```json
{
  "access_token": "jwt-token",
  "token_type": "bearer"
}
```

#### GET `/auth/me`
Get current user information.

**Response:**
```json
{
  "id": "user-id",
  "email": "user@example.com",
  "name": "John Doe",
  "role": "user",
  "background_software": "Software Engineer",
  "background_hardware": "Robotics Enthusiast"
}
```

### Content (`/content`)

#### GET `/content/`
Get list of textbook content.

**Query Parameters:**
- `level`: Filter by level (beginner, intermediate, advanced)
- `limit`: Number of items to return (default: 20)
- `offset`: Offset for pagination (default: 0)

#### GET `/content/{slug}`
Get specific content by slug with associated fun facts.

**Response:**
```json
{
  "id": "content-id",
  "title": "Content Title",
  "slug": "content-slug",
  "content": "Main content text",
  "content_ur": "Urdu translation (optional)",
  "chapter_number": 1,
  "section_number": 1,
  "level": "beginner",
  "prerequisites": ["prereq1", "prereq2"],
  "learning_objectives": ["objective1", "objective2"],
  "is_published": true,
  "fun_fact_cards": [
    {
      "id": "fact-id",
      "content_id": "content-id",
      "title": "Fun Fact Title",
      "description": "Fun fact description",
      "category": "technical",
      "difficulty_level": "beginner"
    }
  ]
}
```

#### GET `/content/{slug}/personalize`
Get personalized content based on user preferences.

#### GET `/content/{slug}/translate/ur`
Get Urdu translation of content.

#### GET `/content/{slug}/fun-facts`
Get fun fact cards for a specific content.

### RAG Chatbot (`/rag`)

#### POST `/rag/chat`
Chat with the RAG system.

**Request Body:**
```json
{
  "message": "Your question here",
  "content_slug": "content-slug",
  "history": []
}
```

**Response:**
```json
{
  "response": "AI response",
  "sources": ["source1", "source2"],
  "confidence": 0.85
}
```

#### POST `/rag/validate`
Validate if a question is relevant to textbook content.

**Request Body:**
```json
{
  "message": "Your question here",
  "content_slug": "content-slug"
}
```

**Response:**
```json
{
  "is_relevant": true
}
```

### User Preferences (`/preferences`)

#### GET `/preferences/theme`
Get user's theme preference.

#### POST `/preferences/theme`
Set user's theme preference.

**Request Body:**
```json
{
  "theme": "light|dark|system"
}
```

#### GET `/preferences/personalization`
Get user's personalization profile.

#### POST `/preferences/personalization`
Set user's personalization profile.

**Request Body:**
```json
{
  "background_software": "Software background",
  "background_hardware": "Hardware background",
  "learning_goals": ["goal1", "goal2"]
}
```

### Admin (`/admin`)

#### GET `/admin/fun-facts`
Get all fun fact cards (admin only).

#### POST `/admin/fun-facts`
Create a new fun fact card (admin only).

#### GET `/admin/fun-facts/{fact_id}`
Get a specific fun fact card (admin only).

#### PUT `/admin/fun-facts/{fact_id}`
Update a fun fact card (admin only).

#### DELETE `/admin/fun-facts/{fact_id}`
Delete a fun fact card (admin only).

#### GET `/admin/fun-facts/content/{content_id}`
Get all fun fact cards for a specific content (admin only).

## Monitoring & Health

#### GET `/health`
Basic health check.

#### GET `/monitoring/health`
Detailed health check with system metrics.

#### GET `/monitoring/metrics`
Get application metrics.

## Error Handling

The API uses standard HTTP status codes:

- `200`: Success
- `201`: Created
- `400`: Bad Request
- `401`: Unauthorized
- `403`: Forbidden
- `404`: Not Found
- `409`: Conflict
- `500`: Internal Server Error

Error responses include a detail field:
```json
{
  "detail": "Error message"
}
```

## Rate Limiting

The API implements rate limiting:
- Auth endpoints: 5 requests per minute
- RAG endpoints: 30 requests per minute
- Other endpoints: 100 requests per minute

## Security

- All sensitive endpoints require authentication
- Rate limiting prevents abuse
- Input validation on all endpoints
- CORS configured for security