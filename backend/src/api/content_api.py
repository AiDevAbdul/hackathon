from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from typing import List, Optional

from ..database import get_db
from ..models.user import User
from ..models.user_progress import UserProgress
from ..models.textbook_content import TextbookContent as TextbookContentModel
from ..models.fun_fact_card import FunFactCard as FunFactCardModel
from ..services.rag_service import RAGService
from ..api.auth_api import get_current_user

router = APIRouter()
rag_service = RAGService()

class FunFactCard(BaseModel):
    id: str
    content_id: str
    title: str
    description: str
    category: str  # historical, technical, application
    difficulty_level: str

class TextbookContent(BaseModel):
    id: str
    title: str
    slug: str
    content: str
    content_ur: Optional[str] = None
    chapter_number: int
    section_number: Optional[int] = None
    level: str  # beginner, intermediate, advanced
    prerequisites: List[str] = []
    learning_objectives: List[str]
    is_published: bool
    fun_fact_cards: List[FunFactCard] = []  # Add fun fact cards to the content model

class ContentResponse(BaseModel):
    items: List[TextbookContent]
    total: int

class PersonalizedContentRequest(BaseModel):
    slug: str
    include_personalization: bool = True

class TranslationRequest(BaseModel):
    slug: str

class TranslationResponse(BaseModel):
    content_id: str
    translated_content: str

@router.get("/", response_model=ContentResponse)
async def get_content_list(
    level: Optional[str] = None,
    limit: int = 20,
    offset: int = 0,
    current_user: User = Depends(get_current_user)
):
    """Get list of textbook content."""
    # This would typically fetch from a database
    # For now, return an empty list as placeholder
    return ContentResponse(items=[], total=0)

@router.get("/{slug}", response_model=TextbookContent)
async def get_content_by_slug(
    slug: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get specific content by slug with associated fun fact cards."""
    from sqlalchemy.future import select

    # Fetch the textbook content
    content_result = await db.execute(
        select(TextbookContentModel)
        .filter(TextbookContentModel.slug == slug)
    )
    content = content_result.scalar_one_or_none()

    if not content:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Content with slug '{slug}' not found"
        )

    # Fetch associated fun fact cards
    fun_facts_result = await db.execute(
        select(FunFactCardModel)
        .filter(FunFactCardModel.content_id == content.id)
        .filter(FunFactCardModel.is_active == True)
    )
    fun_fact_cards = fun_facts_result.scalars().all()

    # Convert SQLAlchemy models to Pydantic models
    fun_fact_pydantic = [
        FunFactCard(
            id=str(fact.id),
            content_id=fact.content_id,
            title=fact.title,
            description=fact.description,
            category=fact.category,
            difficulty_level=fact.difficulty_level
        )
        for fact in fun_fact_cards
    ]

    # Return the content with associated fun fact cards
    return TextbookContent(
        id=content.id,
        title=content.title,
        slug=content.slug,
        content=content.content,
        content_ur=content.content_ur,
        chapter_number=content.chapter_number,
        section_number=content.section_number,
        level=content.level,
        prerequisites=content.prerequisites if content.prerequisites else [],
        learning_objectives=content.learning_objectives if content.learning_objectives else [],
        is_published=content.is_published,
        fun_fact_cards=fun_fact_pydantic
    )

@router.get("/{slug}/personalize", response_model=TextbookContent)
async def get_personalized_content(
    slug: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get personalized content based on user's background and preferences."""
    from ..services.personalization_service import PersonalizationService
    from sqlalchemy.future import select

    try:
        # Fetch the textbook content
        content_result = await db.execute(
            select(TextbookContentModel)
            .filter(TextbookContentModel.slug == slug)
        )
        content = content_result.scalar_one_or_none()

        if not content:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Content with slug '{slug}' not found"
            )

        # Apply personalization to the content
        personalized_content = await PersonalizationService.personalize_content(
            db, current_user.id, content.content
        )

        # Fetch associated fun fact cards
        fun_facts_result = await db.execute(
            select(FunFactCardModel)
            .filter(FunFactCardModel.content_id == content.id)
            .filter(FunFactCardModel.is_active == True)
        )
        fun_fact_cards = fun_facts_result.scalars().all()

        # Convert SQLAlchemy models to Pydantic models
        fun_fact_pydantic = [
            FunFactCard(
                id=str(fact.id),
                content_id=fact.content_id,
                title=fact.title,
                description=fact.description,
                category=fact.category,
                difficulty_level=fact.difficulty_level
            )
            for fact in fun_fact_cards
        ]

        # Return the personalized content with associated fun fact cards
        return TextbookContent(
            id=content.id,
            title=content.title,
            slug=content.slug,
            content=personalized_content,
            content_ur=content.content_ur,
            chapter_number=content.chapter_number,
            section_number=content.section_number,
            level=content.level,
            prerequisites=content.prerequisites if content.prerequisites else [],
            learning_objectives=content.learning_objectives if content.learning_objectives else [],
            is_published=content.is_published,
            fun_fact_cards=fun_fact_pydantic
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error personalizing content: {str(e)}"
        )

@router.get("/{slug}/translate/ur", response_model=TranslationResponse)
async def get_urdu_translation(
    slug: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get Urdu translation of content."""
    from ..services.translation_service import TranslationService

    # This would typically fetch original content from a database
    # For now, we'll use a placeholder content
    # In a real implementation, you would fetch the actual content by slug
    original_content = f"Placeholder content for {slug}"  # This would come from actual content DB

    # Get or create translation
    try:
        translation_service = TranslationService()
        translated_content, confidence = await translation_service.get_or_create_translation(
            db, slug, original_content, "ur"
        )

        return TranslationResponse(
            content_id=slug,
            translated_content=translated_content
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error translating content: {str(e)}"
        )

@router.get("/{slug}/fun-facts", response_model=List[FunFactCard])
async def get_fun_fact_cards(
    slug: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get fun fact cards for a specific content."""
    from ..services.fun_fact_service import FunFactService

    try:
        fun_facts = await FunFactService.get_fun_fact_cards_for_content(db, slug)
        return fun_facts
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching fun fact cards: {str(e)}"
        )

# Include the RAG service initialization endpoint
@router.post("/initialize-rag")
async def initialize_rag_system(current_user: User = Depends(get_current_user)):
    """Initialize the RAG system (admin only)."""
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admin users can initialize RAG system"
        )

    try:
        await rag_service.initialize_rag_system()
        return {"message": "RAG system initialized successfully"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error initializing RAG system: {str(e)}"
        )