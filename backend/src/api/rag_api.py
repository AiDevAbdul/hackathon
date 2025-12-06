from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from typing import List, Optional

# Import rate limiting
from slowapi import Limiter
from slowapi.util import get_remote_address

from ..database import get_db
from ..models.user import User
from ..services.rag_service import RAGService
from ..api.auth_api import get_current_user

# Initialize limiter for this router
limiter = Limiter(key_func=get_remote_address)

router = APIRouter()

class RAGChatRequest(BaseModel):
    message: str
    content_slug: str
    history: Optional[List[dict]] = []

class RAGChatResponse(BaseModel):
    response: str
    sources: List[str]
    confidence: float

class RAGValidateRequest(BaseModel):
    message: str
    content_slug: str

class RAGValidateResponse(BaseModel):
    is_relevant: bool

rag_service = RAGService()

@router.post("/chat", response_model=RAGChatResponse)
@limiter.limit("30/minute")  # Limit RAG chat requests to prevent abuse
async def rag_chat(
    request: RAGChatRequest,
    current_user: User = Depends(get_current_user)
):
    """Chat with the RAG system to get answers based on textbook content."""
    try:
        result = await rag_service.query_rag(
            query=request.message,
            content_slug=request.content_slug
        )
        return RAGChatResponse(**result)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing RAG query: {str(e)}"
        )

@router.post("/validate", response_model=RAGValidateResponse)
@limiter.limit("60/minute")  # Limit RAG validation requests
async def validate_rag_query(
    request: RAGValidateRequest,
    current_user: User = Depends(get_current_user)
):
    """Validate if a question is relevant to the textbook content."""
    try:
        is_relevant = await rag_service.validate_question_relevance(
            question=request.message,
            content_slug=request.content_slug
        )
        return RAGValidateResponse(is_relevant=is_relevant)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error validating RAG query: {str(e)}"
        )

@router.post("/index-content")
async def index_textbook_content(
    content_id: str,
    content: str,
    metadata: dict = None,
    current_user: User = Depends(get_current_user)
):
    """Index textbook content for RAG retrieval (admin only)."""
    # In a real implementation, you would check if the user has admin rights
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admin users can index content"
        )

    try:
        await rag_service.index_content(content_id, content, metadata)
        return {"message": f"Content {content_id} indexed successfully"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error indexing content: {str(e)}"
        )