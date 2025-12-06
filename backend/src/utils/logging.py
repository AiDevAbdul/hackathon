import logging
import sys
from typing import Any
from fastapi import HTTPException
from functools import wraps
import traceback

# Configure the root logger
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('app.log')
    ]
)

def get_logger(name: str) -> logging.Logger:
    """Get a configured logger instance."""
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    return logger

# Create a default logger for the application
app_logger = get_logger(__name__)

class AppException(HTTPException):
    """Custom application exception with detailed logging."""

    def __init__(self, status_code: int, detail: str, error_code: str = None):
        super().__init__(status_code=status_code, detail=detail)
        self.error_code = error_code or f"ERR_{status_code}"
        app_logger.error(f"{self.error_code}: {detail}")

def log_exceptions(func):
    """Decorator to log exceptions in functions."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            app_logger.error(f"Exception in {func.__name__}: {str(e)}")
            app_logger.error(traceback.format_exc())
            raise
    return wrapper

def setup_error_handlers(app):
    """Set up global error handlers for the FastAPI app."""

    @app.exception_handler(Exception)
    async def global_exception_handler(request, exc):
        app_logger.error(f"Global exception: {str(exc)}")
        app_logger.error(traceback.format_exc())
        return {"detail": "Internal server error", "error_code": "INTERNAL_ERROR"}

# Define common loggers for different parts of the application
auth_logger = get_logger("auth")
api_logger = get_logger("api")
rag_logger = get_logger("rag")
db_logger = get_logger("database")