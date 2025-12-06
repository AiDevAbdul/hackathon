# API Contracts: Physical AI & Humanoid Robotics Textbook Platform

**Feature**: 003-dual-platform-setup
**Date**: 2025-12-06
**Version**: 1.0
**Status**: Draft

## Overview

This document defines the API contracts for the Physical AI & Humanoid Robotics Textbook Platform. These contracts establish the interface between the frontend applications (both Docusaurus and Next.js versions) and the backend services.

## Base URLs

- **Development**: `http://localhost:8000/api`
- **Production**: `https://yourdomain.com/api`

## Authentication

Most endpoints require authentication using JWT tokens. Include the token in the Authorization header:

```
Authorization: Bearer <your-jwt-token>
```

Some endpoints (like login and registration) are public and don't require authentication.

## API Endpoints

### 1. Authentication API (`/auth`)

#### POST `/auth/register`
Register a new user account.

**Request Body**:
```json
{
  "email": "user@example.com",
  "password": "securePassword123",
  "name": "John Doe",
  "background_software": "Software Engineer",
  "background_hardware": "Robotics Enthusiast"
}
```

**Response (200)**:
```json
{
  "access_token": "jwt-token-string",
  "token_type": "bearer"
}
```

**Response (409)**: Email already registered
```json
{
  "detail": "Email already registered"
}
```

#### POST `/auth/login`
Login with existing credentials.

**Request Body**:
```json
{
  "email": "user@example.com",
  "password": "securePassword123"
}
```

**Response (200)**:
```json
{
  "access_token": "jwt-token-string",
  "token_type": "bearer"
}
```

**Response (401)**: Invalid credentials
```json
{
  "detail": "Incorrect email or password"
}
```

#### GET `/auth/me`
Get current user information.

**Headers**:
```
Authorization: Bearer <valid-jwt-token>
```

**Response (200)**:
```json
{
  "id": "user-id-uuid",
  "email": "user@example.com",
  "name": "John Doe",
  "role": "student",
  "background_software": "Software Engineer",
  "background_hardware": "Robotics Enthusiast",
  "created_at": "2025-12-06T10:00:00Z",
  "updated_at": "2025-12-06T10:00:00Z",
  "last_login": "2025-12-06T10:00:00Z"
}
```

#### POST `/auth/logout`
Logout the current user.

**Headers**:
```
Authorization: Bearer <valid-jwt-token>
```

**Response (200)**:
```json
{
  "message": "Logged out successfully"
}
```

### 2. Content API (`/content`)

#### GET `/content`
Get list of available textbook content.

**Parameters**:
- `limit` (optional, integer): Number of items to return (default: 20)
- `offset` (optional, integer): Offset for pagination (default: 0)
- `level` (optional, string): Filter by difficulty level (beginner, intermediate, advanced)

**Response (200)**:
```json
{
  "items": [
    {
      "id": "content-id-uuid",
      "title": "Introduction to Physical AI",
      "slug": "introduction-to-physical-ai",
      "chapter_number": 1,
      "section_number": 1,
      "level": "beginner",
      "is_published": true,
      "created_at": "2025-12-06T10:00:00Z"
    }
  ],
  "total": 12,
  "limit": 20,
  "offset": 0
}
```

#### GET `/content/{slug}`
Get specific textbook content by slug.

**Path Parameters**:
- `slug` (string): URL-friendly identifier for the content

**Response (200)**:
```json
{
  "id": "content-id-uuid",
  "title": "Introduction to Physical AI",
  "slug": "introduction-to-physical-ai",
  "content": "# Introduction to Physical AI...",
  "content_ur": "# متعارفہ فزیکل اے آئی...",
  "chapter_number": 1,
  "section_number": 1,
  "level": "beginner",
  "prerequisites": [],
  "learning_objectives": [
    "Understand the basics of Physical AI",
    "Recognize key components of humanoid robotics"
  ],
  "is_published": true,
  "created_at": "2025-12-06T10:00:00Z",
  "updated_at": "2025-12-06T10:00:00Z",
  "fun_fact_cards": [
    {
      "id": "fact-id-uuid",
      "title": "Historical Milestone",
      "description": "The first humanoid robot was created in...",
      "category": "historical",
      "difficulty_level": "beginner",
      "position": "inline"
    }
  ]
}
```

#### GET `/content/{slug}/personalize`
Get personalized content based on user's background and preferences.

**Headers**:
```
Authorization: Bearer <valid-jwt-token>
```

**Path Parameters**:
- `slug` (string): URL-friendly identifier for the content

**Response (200)**:
```json
{
  "original_content": "...",
  "personalized_content": "...",
  "personalization_applied": {
    "complexity_adjusted": true,
    "examples_modified": true,
    "examples_type": "software-oriented"
  }
}
```

#### GET `/content/{slug}/translate/{language}`
Get translated content (currently supports 'ur' for Urdu).

**Path Parameters**:
- `slug` (string): URL-friendly identifier for the content
- `language` (string): Target language code ('ur' for Urdu)

**Headers**:
```
Authorization: Bearer <valid-jwt-token>
```

**Response (200)**:
```json
{
  "original_content": "# Introduction to Physical AI...",
  "translated_content": "# متعارفہ فزیکل اے آئی...",
  "source_language": "en",
  "target_language": "ur",
  "translation_confidence": 0.85,
  "translation_source": "ai_model_name",
  "cached": true
}
```

#### GET `/content/{slug}/fun-facts`
Get fun fact cards associated with specific content.

**Path Parameters**:
- `slug` (string): URL-friendly identifier for the content

**Response (200)**:
```json
{
  "fun_fact_cards": [
    {
      "id": "fact-id-uuid",
      "title": "Historical Milestone",
      "description": "The first humanoid robot was created in...",
      "category": "historical",
      "difficulty_level": "beginner",
      "position": "inline",
      "created_at": "2025-12-06T10:00:00Z"
    }
  ]
}
```

### 3. RAG Chatbot API (`/rag`)

#### POST `/rag/chat`
Chat with the RAG system to get answers based on textbook content.

**Headers**:
```
Authorization: Bearer <valid-jwt-token>
Content-Type: application/json
```

**Request Body**:
```json
{
  "message": "What is ROS 2?",
  "content_slug": "ros2-the-robotic-nervous-system",  // Optional, limits to specific content
  "history": []  // Optional, conversation history
}
```

**Response (200)**:
```json
{
  "response": "ROS 2 (Robot Operating System 2) is a flexible framework for...",
  "sources": [
    {
      "content_id": "content-id-uuid",
      "title": "The Robotic Nervous System",
      "section": "Introduction to ROS 2",
      "relevance_score": 0.87
    }
  ],
  "confidence": 0.92,
  "processing_time_ms": 1250
}
```

#### POST `/rag/validate`
Validate if a question is relevant to textbook content.

**Headers**:
```
Authorization: Bearer <valid-jwt-token>
Content-Type: application/json
```

**Request Body**:
```json
{
  "message": "What is ROS 2?",
  "content_slug": "ros2-the-robotic-nervous-system"
}
```

**Response (200)**:
```json
{
  "is_relevant": true,
  "confidence": 0.95,
  "relevant_topics": [
    "ROS 2 Architecture",
    "Node Communication",
    "Message Passing"
  ]
}
```

### 4. User Preferences API (`/preferences`)

#### GET `/preferences/theme`
Get user's theme preference.

**Headers**:
```
Authorization: Bearer <valid-jwt-token>
```

**Response (200)**:
```json
{
  "theme_mode": "system",
  "updated_at": "2025-12-06T10:00:00Z"
}
```

#### POST `/preferences/theme`
Set user's theme preference.

**Headers**:
```
Authorization: Bearer <valid-jwt-token>
Content-Type: application/json
```

**Request Body**:
```json
{
  "theme_mode": "dark"
}
```

**Response (200)**:
```json
{
  "theme_mode": "dark",
  "updated_at": "2025-12-06T10:00:00Z"
}
```

#### GET `/preferences/personalization`
Get user's personalization profile.

**Headers**:
```
Authorization: Bearer <valid-jwt-token>
```

**Response (200)**:
```json
{
  "content_level_preference": "intermediate",
  "example_preference": "practical",
  "detail_preference": "detailed",
  "learning_path": ["module1", "module2"],
  "updated_at": "2025-12-06T10:00:00Z"
}
```

#### POST `/preferences/personalization`
Set user's personalization profile.

**Headers**:
```
Authorization: Bearer <valid-jwt-token>
Content-Type: application/json
```

**Request Body**:
```json
{
  "content_level_preference": "intermediate",
  "example_preference": "practical",
  "detail_preference": "detailed",
  "learning_path": ["module1", "module2"]
}
```

**Response (200)**:
```json
{
  "content_level_preference": "intermediate",
  "example_preference": "practical",
  "detail_preference": "detailed",
  "learning_path": ["module1", "module2"],
  "updated_at": "2025-12-06T10:00:00Z"
}
```

### 5. User Progress API (`/progress`)

#### GET `/progress`
Get user's learning progress.

**Headers**:
```
Authorization: Bearer <valid-jwt-token>
```

**Response (200)**:
```json
{
  "progress_records": [
    {
      "content_id": "content-id-uuid",
      "content_title": "Introduction to Physical AI",
      "status": "completed",
      "completion_percentage": 100.0,
      "time_spent_seconds": 1200,
      "last_accessed": "2025-12-06T10:00:00Z",
      "notes": "Great chapter on fundamentals"
    }
  ]
}
```

#### POST `/progress/{content_id}`
Update progress for specific content.

**Headers**:
```
Authorization: Bearer <valid-jwt-token>
Content-Type: application/json
```

**Path Parameters**:
- `content_id` (string): ID of the content being progressed

**Request Body**:
```json
{
  "status": "in_progress",
  "completion_percentage": 75.0,
  "notes": "Currently studying the RAG implementation"
}
```

**Response (200)**:
```json
{
  "content_id": "content-id-uuid",
  "status": "in_progress",
  "completion_percentage": 75.0,
  "last_accessed": "2025-12-06T10:00:00Z",
  "updated_at": "2025-12-06T10:00:00Z"
}
```

### 6. Admin API (`/admin`)

#### GET `/admin/fun-facts`
Get all fun fact cards (admin only).

**Headers**:
```
Authorization: Bearer <valid-admin-jwt-token>
```

**Response (200)**:
```json
{
  "fun_fact_cards": [
    {
      "id": "fact-id-uuid",
      "content_id": "content-id-uuid",
      "title": "Historical Milestone",
      "description": "The first humanoid robot was created in...",
      "category": "historical",
      "difficulty_level": "beginner",
      "position": "inline",
      "is_active": true,
      "created_at": "2025-12-06T10:00:00Z",
      "updated_at": "2025-12-06T10:00:00Z"
    }
  ]
}
```

#### POST `/admin/fun-facts`
Create a new fun fact card (admin only).

**Headers**:
```
Authorization: Bearer <valid-admin-jwt-token>
Content-Type: application/json
```

**Request Body**:
```json
{
  "content_id": "content-id-uuid",
  "title": "New Fun Fact",
  "description": "An interesting fact about humanoid robotics...",
  "category": "technical",
  "difficulty_level": "intermediate",
  "position": "sidebar"
}
```

**Response (201)**:
```json
{
  "id": "new-fact-id-uuid",
  "content_id": "content-id-uuid",
  "title": "New Fun Fact",
  "description": "An interesting fact about humanoid robotics...",
  "category": "technical",
  "difficulty_level": "intermediate",
  "position": "sidebar",
  "is_active": true,
  "created_at": "2025-12-06T10:00:00Z",
  "updated_at": "2025-12-06T10:00:00Z"
}
```

### 7. Health Check API (`/health`)

#### GET `/health`
Basic health check for the API.

**Response (200)**:
```json
{
  "status": "healthy",
  "service": "textbook-platform-api",
  "version": "1.0.0",
  "timestamp": "2025-12-06T10:00:00Z"
}
```

#### GET `/monitoring/health`
Detailed health check with system metrics.

**Response (200)**:
```json
{
  "status": "healthy",
  "service": "textbook-platform-api",
  "timestamp": "2025-12-06T10:00:00Z",
  "memory_usage": 45.2,
  "cpu_usage": 12.8,
  "disk_usage": 65.4,
  "uptime": "2h 15m 30s",
  "database_status": "connected",
  "vector_db_status": "connected",
  "cache_status": "connected"
}
```

## Error Handling

### Standard Error Format

All error responses follow this format:

```json
{
  "detail": "Human-readable error message"
}
```

### Common HTTP Status Codes

- **200**: Success
- **201**: Created
- **400**: Bad Request (invalid input)
- **401**: Unauthorized (missing or invalid authentication)
- **403**: Forbidden (insufficient permissions)
- **404**: Not Found
- **409**: Conflict (resource already exists)
- **422**: Unprocessable Entity (validation error)
- **429**: Too Many Requests (rate limit exceeded)
- **500**: Internal Server Error

## Rate Limiting

API endpoints are subject to rate limiting:

- **Authentication endpoints**: 5 requests per minute
- **RAG endpoints**: 30 requests per minute
- **Other endpoints**: 100 requests per minute

When rate limited, the response will include:
- Status code: 429
- Headers: `Retry-After` indicating seconds to wait
- Body: Standard error format with rate limit message

## Security Headers

All API responses include security headers:
- `Strict-Transport-Security`: For HTTPS enforcement
- `X-Content-Type-Options`: To prevent MIME type sniffing
- `X-Frame-Options`: To prevent clickjacking
- `X-XSS-Protection`: For XSS protection

## Versioning

The API uses URI versioning. Current version is v1, accessed via `/api/v1/*` endpoints.

## Data Formats

### Dates and Times
All timestamps are in ISO 8601 format in UTC: `YYYY-MM-DDTHH:MM:SSZ`

### Text Content
Text content is in Markdown format unless otherwise specified.

### Language Codes
Language codes follow ISO 639-1 standard:
- `en`: English
- `ur`: Urdu
- `hi`: Hindi
- `ar`: Arabic

## Validation Rules

### Request Validation
- All string fields are trimmed of leading/trailing whitespace
- Email fields are validated for proper format
- Numeric fields must be within specified ranges
- Required fields must be present

### Content Validation
- Content must be between 10 and 10,000 characters
- Titles must be between 1 and 200 characters
- Slugs must be URL-friendly (lowercase, hyphens only)