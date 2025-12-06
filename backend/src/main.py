from datetime import datetime
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from contextlib import asynccontextmanager
import logging

# Import rate limiting
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

from .api.auth_api import router as auth_router
from .api.rag_api import router as rag_router
from .api.content_api import router as content_router
from .api.user_preferences_api import router as user_preferences_router
from .api.admin_api import router as admin_router
from .config.settings import settings
from .utils.logging import app_logger

# Initialize rate limiter
limiter = Limiter(key_func=get_remote_address)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    app_logger.info("Starting up the application...")
    # Here you can initialize database connections, etc.
    # For example, initialize Qdrant collection, etc.

    yield

    # Shutdown
    app_logger.info("Shutting down the application...")

app = FastAPI(
    title="Physical AI & Humanoid Robotics Textbook Platform API",
    description="API for the textbook platform with authentication, RAG chatbot, personalization, and translation features",
    version="1.0.0",
    lifespan=lifespan,
    # Add security headers
    docs_url="/docs" if settings.DEBUG else None,
    redoc_url="/redoc" if settings.DEBUG else None,
)

# Add security middleware
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=settings.ALLOWED_HOSTS if settings.ALLOWED_HOSTS else ["localhost", "127.0.0.1", "0.0.0.0"]
)

# Add CORS middleware with enhanced security
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS if settings.ALLOWED_ORIGINS else ["http://localhost:3000", "http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
    allow_headers=["*"],
    # Add additional security options
    allow_origin_regex=None,
    expose_headers=["Access-Control-Allow-Origin"],
    max_age=600,
)

# Set up rate limiting
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Include routers with rate limiting
app.include_router(auth_router, prefix="/auth", tags=["Authentication"])
app.include_router(rag_router, prefix="/rag", tags=["RAG Chatbot"])
app.include_router(content_router, prefix="/content", tags=["Content"])
app.include_router(user_preferences_router, prefix="/preferences", tags=["User Preferences"])
app.include_router(admin_router, prefix="/admin", tags=["Admin"])

@app.get("/")
def read_root():
    app_logger.info("Root endpoint accessed")
    return {"message": "Welcome to the Physical AI & Humanoid Robotics Textbook Platform API"}

@app.get("/health")
def health_check():
    app_logger.info("Health check endpoint accessed")
    return {"status": "healthy", "service": "textbook-platform-api"}

@app.get("/monitoring/health")
def detailed_health_check():
    """Detailed health check with additional metrics."""
    import psutil
    import os

    health_info = {
        "status": "healthy",
        "service": "textbook-platform-api",
        "timestamp": datetime.utcnow().isoformat(),
        "memory_usage": psutil.virtual_memory().percent,
        "cpu_usage": psutil.cpu_percent(interval=1),
        "disk_usage": psutil.disk_usage("/").percent if os.name != "nt" else "N/A (Windows)",
        "uptime": "N/A"  # This would require tracking since app start
    }
    app_logger.info("Detailed health check accessed")
    return health_info

@app.get("/monitoring/metrics")
def get_metrics():
    """Get application metrics."""
    metrics = {
        "service": "textbook-platform-api",
        "version": "1.0.0",
        "endpoints_count": len(app.routes),
        "timestamp": datetime.utcnow().isoformat()
    }
    app_logger.info("Metrics endpoint accessed")
    return metrics