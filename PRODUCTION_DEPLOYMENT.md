# Physical AI & Humanoid Robotics Textbook Platform - Production Deployment Guide

## Overview

This document provides instructions for deploying the Physical AI & Humanoid Robotics Textbook Platform to a production environment.

## Prerequisites

### Infrastructure Requirements
- Docker and Docker Compose installed
- At least 4GB RAM available
- 20GB disk space for application and data
- SSL certificate for HTTPS
- Domain name configured to point to your server

### Environment Variables
Before deployment, prepare the following environment variables:

#### Backend (.env file)
```bash
# Database Configuration
DATABASE_URL=postgresql://user:password@db:5432/textbook_platform

# Security
SECRET_KEY=your-super-secret-key-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# OpenAI Configuration
OPENAI_API_KEY=your-openai-api-key

# Qdrant Configuration
QDRANT_HOST=qdrant
QDRANT_PORT=6333

# Application Settings
DEBUG=False
ALLOWED_ORIGINS=https://yourdomain.com
ALLOWED_HOSTS=yourdomain.com,localhost
```

#### Frontend (.env file)
```bash
REACT_APP_API_URL=https://yourdomain.com
REACT_APP_ENV=production
```

## Deployment Steps

### 1. Clone the Repository
```bash
git clone https://github.com/your-organization/textbook-platform.git
cd textbook-platform
```

### 2. Configure Environment Variables
Create `.env` files for both frontend and backend with your production values:

```bash
# Create backend environment file
cat > .env << EOF
DATABASE_URL=postgresql://user:password@db:5432/textbook_platform
SECRET_KEY=your-production-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
OPENAI_API_KEY=your-openai-api-key
QDRANT_HOST=qdrant
QDRANT_PORT=6333
DEBUG=False
ALLOWED_ORIGINS=https://yourdomain.com
ALLOWED_HOSTS=yourdomain.com,localhost
EOF
```

### 3. Update Docker Compose for Production
Create a production-specific docker-compose file:

```bash
# docker-compose.prod.yml
version: '3.8'

services:
  backend:
    build:
      context: .
      dockerfile: backend/Dockerfile
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:password@db:5432/textbook_platform
      - SECRET_KEY=${SECRET_KEY}
      - ALGORITHM=HS256
      - ACCESS_TOKEN_EXPIRE_MINUTES=30
      - QDRANT_HOST=qdrant
      - QDRANT_PORT=6333
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - DEBUG=False
      - ALLOWED_ORIGINS=https://yourdomain.com
    depends_on:
      - db
      - qdrant
    restart: unless-stopped
    networks:
      - app-network

  frontend:
    build:
      context: .
      dockerfile: frontend/Dockerfile
    ports:
      - "3000:3000"
    environment:
      - REACT_APP_API_URL=https://yourdomain.com
    depends_on:
      - backend
    restart: unless-stopped
    networks:
      - app-network

  db:
    image: postgres:15
    environment:
      POSTGRES_DB: textbook_platform
      POSTGRES_USER: user
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    restart: unless-stopped
    networks:
      - app-network

  qdrant:
    image: qdrant/qdrant:latest
    volumes:
      - qdrant_data:/qdrant/storage
    restart: unless-stopped
    networks:
      - app-network

networks:
  app-network:
    driver: bridge

volumes:
  postgres_data:
  qdrant_data:
```

### 4. Set Up Reverse Proxy (Nginx)
Create an Nginx configuration to serve the application:

```nginx
# /etc/nginx/sites-available/textbook-platform
server {
    listen 80;
    server_name yourdomain.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name yourdomain.com;

    ssl_certificate /path/to/your/certificate.crt;
    ssl_certificate_key /path/to/your/private.key;

    location / {
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;
    }

    location /api/ {
        proxy_pass http://localhost:8000/;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /health {
        proxy_pass http://localhost:8000/health;
    }

    location /monitoring/ {
        proxy_pass http://localhost:8000/monitoring/;
    }
}
```

### 5. Deploy the Application
```bash
# Build and start the services
docker-compose -f docker-compose.prod.yml up -d --build

# Verify services are running
docker-compose -f docker-compose.prod.yml ps
```

### 6. Run Database Migrations
```bash
# Access the backend container and run migrations
docker-compose -f docker-compose.prod.yml exec backend python -m alembic upgrade head
```

### 7. Initialize RAG System
```bash
# Initialize the RAG system by calling the API endpoint
curl -X POST https://yourdomain.com/api/v1/content/initialize-rag \
  -H "Authorization: Bearer your-admin-token"
```

## Security Considerations

### HTTPS Setup
- Use Let's Encrypt for free SSL certificates
- Enable HSTS headers
- Configure proper SSL protocols and ciphers

### API Security
- Rate limiting is enabled by default
- Authentication required for all protected endpoints
- Input validation on all endpoints
- SQL injection protection through SQLAlchemy

### Data Protection
- Database encryption at rest
- API keys stored as environment variables
- Regular backup procedures implemented
- Access logging enabled

## Monitoring and Maintenance

### Health Checks
- `/health` - Basic health check
- `/monitoring/health` - Detailed system metrics
- `/monitoring/metrics` - Application metrics

### Backup Procedures
Run the backup script regularly:
```bash
python backup_script.py create
```

### Log Management
- Application logs are written to `app.log`
- Configure log rotation for production
- Monitor logs for errors and performance issues

## Performance Optimization

### Caching
- Translation caching implemented
- RAG query caching with TTL
- Database query optimization

### CDN Setup
Consider using a CDN for:
- Static assets (images, CSS, JS)
- API response caching
- Global content delivery

## Troubleshooting

### Common Issues

#### Database Connection Issues
- Verify PostgreSQL is running
- Check database credentials
- Ensure network connectivity between services

#### API Key Issues
- Verify OpenAI API key is valid
- Check API usage limits
- Ensure proper environment variable configuration

#### Memory Issues
- Monitor application memory usage
- Increase container memory limits if needed
- Check for memory leaks in long-running processes

### Support Contact
For production issues, contact:
- Email: support@yourdomain.com
- Monitoring: /monitoring/health endpoint
- Logs: Check container logs with `docker logs`

## Rollback Procedure

In case of deployment issues:

1. **Immediate Response**
   ```bash
   # Stop the current deployment
   docker-compose -f docker-compose.prod.yml down

   # If needed, start previous version
   docker-compose -f docker-compose.prev.yml up -d
   ```

2. **Database Rollback**
   ```bash
   # Rollback database migrations if needed
   docker-compose exec backend python -m alembic downgrade -1
   ```

## Scaling Recommendations

### Horizontal Scaling
- Load balancer for multiple backend instances
- Read replicas for database
- Multiple RAG service instances

### Vertical Scaling
- Increase container resources
- Optimize database performance
- Upgrade server specifications

## Post-Deployment Tasks

### 1. Verify Deployment
- Test all API endpoints
- Verify user registration/login
- Test RAG chatbot functionality
- Check translation features
- Validate theme switching

### 2. Set Up Monitoring
- Configure alerts for system metrics
- Set up application performance monitoring
- Implement user activity tracking
- Configure error tracking

### 3. Documentation Updates
- Update API documentation with production URLs
- Document deployment procedures
- Create runbooks for common operations
- Prepare incident response procedures

## Conclusion

The Physical AI & Humanoid Robotics Textbook Platform is now ready for production use. All features have been tested and deployed with appropriate security, performance, and monitoring measures in place.