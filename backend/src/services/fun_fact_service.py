from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from uuid import UUID

from ..models.fun_fact_card import FunFactCard

class FunFactService:
    @staticmethod
    async def get_fun_fact_cards_for_content(db: AsyncSession, content_id: str) -> List[FunFactCard]:
        """Get all fun fact cards for a specific content."""
        result = await db.execute(
            select(FunFactCard)
            .filter(FunFactCard.content_id == content_id)
            .filter(FunFactCard.is_active == True)
        )
        return result.scalars().all()

    @staticmethod
    async def get_fun_fact_card_by_id(db: AsyncSession, fact_id: UUID) -> Optional[FunFactCard]:
        """Get a specific fun fact card by ID."""
        result = await db.execute(
            select(FunFactCard)
            .filter(FunFactCard.id == fact_id)
            .filter(FunFactCard.is_active == True)
        )
        return result.scalar_one_or_none()

    @staticmethod
    async def create_fun_fact_card(
        db: AsyncSession,
        content_id: str,
        title: str,
        description: str,
        category: str,
        difficulty_level: str
    ) -> FunFactCard:
        """Create a new fun fact card."""
        fact_card = FunFactCard(
            content_id=content_id,
            title=title,
            description=description,
            category=category,
            difficulty_level=difficulty_level,
            is_active=True
        )
        db.add(fact_card)
        await db.commit()
        await db.refresh(fact_card)
        return fact_card

    @staticmethod
    async def update_fun_fact_card(
        db: AsyncSession,
        fact_id: UUID,
        title: Optional[str] = None,
        description: Optional[str] = None,
        category: Optional[str] = None,
        difficulty_level: Optional[str] = None,
        is_active: Optional[bool] = None
    ) -> Optional[FunFactCard]:
        """Update a fun fact card."""
        fact_card = await FunFactService.get_fun_fact_card_by_id(db, fact_id)
        if not fact_card:
            return None

        if title is not None:
            fact_card.title = title
        if description is not None:
            fact_card.description = description
        if category is not None:
            fact_card.category = category
        if difficulty_level is not None:
            fact_card.difficulty_level = difficulty_level
        if is_active is not None:
            fact_card.is_active = is_active

        await db.commit()
        await db.refresh(fact_card)
        return fact_card

    @staticmethod
    async def delete_fun_fact_card(db: AsyncSession, fact_id: UUID) -> bool:
        """Delete (deactivate) a fun fact card."""
        fact_card = await FunFactService.get_fun_fact_card_by_id(db, fact_id)
        if not fact_card:
            return False

        fact_card.is_active = False  # Soft delete
        await db.commit()
        return True

    @staticmethod
    async def get_fun_fact_cards_by_category(
        db: AsyncSession,
        category: str
    ) -> List[FunFactCard]:
        """Get fun fact cards by category."""
        result = await db.execute(
            select(FunFactCard)
            .filter(FunFactCard.category == category)
            .filter(FunFactCard.is_active == True)
        )
        return result.scalars().all()

    @staticmethod
    async def get_fun_fact_cards_by_difficulty(
        db: AsyncSession,
        difficulty_level: str
    ) -> List[FunFactCard]:
        """Get fun fact cards by difficulty level."""
        result = await db.execute(
            select(FunFactCard)
            .filter(FunFactCard.difficulty_level == difficulty_level)
            .filter(FunFactCard.is_active == True)
        )
        return result.scalars().all()