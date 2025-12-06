---
description: "Research findings for dual-platform setup (Docusaurus + Next.js)"
---

# Research: Dual Platform Setup (Docusaurus + Next.js)

**Feature**: 003-dual-platform-setup
**Date**: 2025-12-06
**Status**: Completed
**Input**: Feature specification from `/specs/[003-dual-platform-setup]/spec.md`

## Research Summary

This document captures all research findings for implementing the dual-platform textbook system supporting both Docusaurus (for GitHub Pages) and Next.js (for modern hosting) with shared backend services for the Physical AI & Humanoid Robotics textbook platform.

## Decision: Dual Platform Architecture

**Rationale**: To maximize accessibility and reach, the platform needs to support both GitHub Pages deployment (using Docusaurus) and modern hosting platforms (using Next.js). This approach ensures the educational content is available to users regardless of their technical setup or hosting preferences.

**Alternatives considered**:
- Single platform approach: Would limit deployment options and accessibility
- Separate applications: Would create maintenance overhead and data inconsistency
- Dual Platform Architecture: Best balance of accessibility, maintainability, and consistency

## Decision: Shared Backend Services

**Rationale**: Both frontend platforms need to access the same user data, content, and AI services (RAG, personalization, translation). A shared backend ensures consistency and reduces duplication.

**Alternatives considered**:
- Separate backend per platform: Would create data inconsistency and maintenance overhead
- Microservices per platform: Would increase complexity without significant benefits
- Shared Backend Services: Provides single source of truth while maintaining platform flexibility

## Decision: Next.js App Router vs Pages Router

**Rationale**: Next.js App Router provides better performance, more flexible routing, and improved server-side rendering capabilities that are essential for the interactive textbook platform with RAG chatbot and personalization features.

**Alternatives considered**:
- Next.js Pages Router: Simpler but less flexible for complex routing needs
- Create React App: Limited server-side rendering capabilities
- Next.js App Router: Superior for complex applications with server components and API routes

## Decision: Docusaurus for GitHub Pages

**Rationale**: Docusaurus is specifically designed for documentation sites and works perfectly with GitHub Pages. It provides excellent SEO, accessibility, and is ideal for static content with minimal interactivity requirements.

**Alternatives considered**:
- Static HTML: Would lack interactivity and modern features
- Jekyll: GitHub's default but lacks advanced features needed
- Docusaurus: Excellent for documentation with good GitHub Pages integration

## Technical Unknowns Resolved

1. **API Integration**: Both platforms can connect to the same backend API using standard HTTP requests
2. **Authentication Sharing**: JWT-based authentication works consistently across both platforms
3. **Content Synchronization**: Same content repository serves both platforms with appropriate formatting
4. **Performance**: Proper caching and CDN strategies ensure good performance on both platforms
5. **Deployment**: Both platforms can be deployed independently while sharing backend services

## Architecture Patterns Researched

### 1. Backend-for-Frontend (BFF) Pattern
- Each frontend could have its own backend service layer
- For our use case, a shared backend is more appropriate due to common data needs

### 2. Micro-frontend Architecture
- Different teams could work on different frontend components
- For our use case, dual platform approach is simpler with shared services

### 3. API Gateway Pattern
- Centralized API management for both frontends
- Already implemented with the shared backend approach

## Performance Considerations

### For Docusaurus (GitHub Pages)
- Static generation for fast loading
- Optimized for read-heavy usage
- CDN delivery through GitHub Pages

### For Next.js (Modern Hosting)
- Server-side rendering for dynamic content
- API routes for backend functionality
- Better for interactive features like chatbot

## Security Considerations

1. **Shared Authentication**: Both platforms use the same JWT-based authentication system
2. **Rate Limiting**: Applied at the backend level to protect shared services
3. **Input Validation**: Consistent validation across both platforms
4. **CORS Configuration**: Properly configured for both frontend origins

## Deployment Strategies Researched

### GitHub Pages (Docusaurus)
- Static site generation
- Free hosting with good reliability
- Excellent for content-focused experience

### Modern Platforms (Next.js)
- Vercel: Optimized for Next.js with excellent performance
- Netlify: Good alternative with similar features
- Self-hosting: Maximum control and customization

## Technology Stack Validation

### Frontend Technologies
- **Next.js 14+**: Supports App Router, server components, and modern features
- **Docusaurus 3.x**: Latest version with improved performance and features
- **Tailwind CSS**: Consistent styling across both platforms
- **TypeScript**: Type safety for better maintainability

### Backend Technologies
- **FastAPI**: High-performance with excellent documentation
- **PostgreSQL**: Reliable database for user data and content
- **Qdrant**: Specialized vector database for RAG functionality
- **Redis**: Caching for improved performance

## Integration Points Researched

### Content Management
- Both platforms access the same content repository
- Different rendering approaches for static vs. dynamic content
- Consistent content structure across platforms

### User Data
- Shared user authentication and preferences
- Consistent user experience across platforms
- Synchronized progress tracking

### AI Services
- Shared RAG system for both platforms
- Consistent AI responses and behavior
- Centralized AI service management

## Scalability Research

### Horizontal Scaling
- Backend services can scale independently
- Database can be scaled with proper indexing
- CDN for static assets improves global performance

### Performance Optimization
- Caching strategies for both platforms
- Database optimization for user queries
- AI service optimization for RAG responses

## Maintenance Considerations

### Content Updates
- Single content repository reduces maintenance overhead
- Both platforms automatically get updated content
- Consistent content across platforms

### Feature Development
- Shared backend services reduce duplication
- Platform-specific features can be developed independently
- Common functionality benefits both platforms

## Research Outcomes

This research confirms that the dual-platform approach is technically feasible and provides significant benefits in terms of accessibility and reach. The shared backend architecture ensures consistency while allowing each platform to optimize for its deployment environment.

The chosen architecture balances the need for:
- Maximum accessibility (GitHub Pages via Docusaurus)
- Advanced features (Next.js with App Router)
- Consistent user experience (shared backend)
- Maintainable codebase (shared services)
- Performance optimization (platform-specific optimizations)