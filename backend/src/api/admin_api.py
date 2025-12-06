from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from typing import List, Optional
import uuid

from ..database import get_db
from ..models.user import User
from ..models.fun_fact_card import FunFactCard as FunFactCardModel
from ..api.auth_api import get_current_user


router = APIRouter()


class FunFactCardCreate(BaseModel):
    content_id: str
    title: str
    description: str
    category: str  # historical, technical, application
    difficulty_level: str  # beginner, intermediate, advanced


class FunFactCardUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    difficulty_level: Optional[str] = None
    is_active: Optional[bool] = None


class FunFactCardResponse(BaseModel):
    id: str
    content_id: str
    title: str
    description: str
    category: str
    difficulty_level: str
    is_active: bool


@router.get("/fun-facts", response_model=List[FunFactCardResponse])
async def get_all_fun_facts(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get all fun fact cards (admin only)."""
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admin users can access this endpoint"
        )

    from sqlalchemy.future import select

    result = await db.execute(
        select(FunFactCardModel)
    )
    fun_facts = result.scalars().all()

    return [
        FunFactCardResponse(
            id=str(fact.id),
            content_id=fact.content_id,
            title=fact.title,
            description=fact.description,
            category=fact.category,
            difficulty_level=fact.difficulty_level,
            is_active=fact.is_active
        )
        for fact in fun_facts
    ]


@router.post("/fun-facts", response_model=FunFactCardResponse)
async def create_fun_fact(
    fact_data: FunFactCardCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Create a new fun fact card (admin only)."""
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admin users can create fun fact cards"
        )

    from sqlalchemy.future import select

    # Create new fun fact card
    new_fact = FunFactCardModel(
        content_id=fact_data.content_id,
        title=fact_data.title,
        description=fact_data.description,
        category=fact_data.category,
        difficulty_level=fact_data.difficulty_level,
        is_active=True  # Default to active
    )

    db.add(new_fact)
    await db.commit()
    await db.refresh(new_fact)

    return FunFactCardResponse(
        id=str(new_fact.id),
        content_id=new_fact.content_id,
        title=new_fact.title,
        description=new_fact.description,
        category=new_fact.category,
        difficulty_level=new_fact.difficulty_level,
        is_active=new_fact.is_active
    )


@router.get("/fun-facts/{fact_id}", response_model=FunFactCardResponse)
async def get_fun_fact(
    fact_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get a specific fun fact card by ID (admin only)."""
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admin users can access this endpoint"
        )

    from sqlalchemy.future import select

    try:
        uuid.UUID(fact_id)  # Validate UUID format
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid fact ID format"
        )

    result = await db.execute(
        select(FunFactCardModel)
        .filter(FunFactCardModel.id == fact_id)
    )
    fact = result.scalar_one_or_none()

    if not fact:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Fun fact with ID '{fact_id}' not found"
        )

    return FunFactCardResponse(
        id=str(fact.id),
        content_id=fact.content_id,
        title=fact.title,
        description=fact.description,
        category=fact.category,
        difficulty_level=fact.difficulty_level,
        is_active=fact.is_active
    )


@router.put("/fun-facts/{fact_id}", response_model=FunFactCardResponse)
async def update_fun_fact(
    fact_id: str,
    fact_data: FunFactCardUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Update a fun fact card (admin only)."""
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admin users can update fun fact cards"
        )

    from sqlalchemy.future import select

    try:
        uuid.UUID(fact_id)  # Validate UUID format
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid fact ID format"
        )

    result = await db.execute(
        select(FunFactCardModel)
        .filter(FunFactCardModel.id == fact_id)
    )
    fact = result.scalar_one_or_none()

    if not fact:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Fun fact with ID '{fact_id}' not found"
        )

    # Update fields that were provided
    if fact_data.title is not None:
        fact.title = fact_data.title
    if fact_data.description is not None:
        fact.description = fact_data.description
    if fact_data.category is not None:
        fact.category = fact_data.category
    if fact_data.difficulty_level is not None:
        fact.difficulty_level = fact_data.difficulty_level
    if fact_data.is_active is not None:
        fact.is_active = fact_data.is_active

    await db.commit()
    await db.refresh(fact)

    return FunFactCardResponse(
        id=str(fact.id),
        content_id=fact.content_id,
        title=fact.title,
        description=fact.description,
        category=fact.category,
        difficulty_level=fact.difficulty_level,
        is_active=fact.is_active
    )


@router.delete("/fun-facts/{fact_id}")
async def delete_fun_fact(
    fact_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Delete a fun fact card (admin only)."""
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admin users can delete fun fact cards"
        )

    from sqlalchemy.future import select

    try:
        uuid.UUID(fact_id)  # Validate UUID format
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid fact ID format"
        )

    result = await db.execute(
        select(FunFactCardModel)
        .filter(FunFactCardModel.id == fact_id)
    )
    fact = result.scalar_one_or_none()

    if not fact:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Fun fact with ID '{fact_id}' not found"
        )

    await db.delete(fact)
    await db.commit()

    return {"message": f"Fun fact with ID '{fact_id}' deleted successfully"}


@router.get("/fun-facts/content/{content_id}", response_model=List[FunFactCardResponse])
async def get_fun_facts_by_content(
    content_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get all fun fact cards for a specific content (admin only)."""
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admin users can access this endpoint"
        )

    from sqlalchemy.future import select

    result = await db.execute(
        select(FunFactCardModel)
        .filter(FunFactCardModel.content_id == content_id)
    )
    fun_facts = result.scalars().all()

    return [
        FunFactCardResponse(
            id=str(fact.id),
            content_id=fact.content_id,
            title=fact.title,
            description=fact.description,
            category=fact.category,
            difficulty_level=fact.difficulty_level,
            is_active=fact.is_active
        )
        for fact in fun_facts
    ]