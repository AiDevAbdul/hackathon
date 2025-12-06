from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from uuid import UUID

from ..models.user import User
from ..services.theme_service import ThemeService

class UserService:
    @staticmethod
    async def get_user_by_id(db: AsyncSession, user_id: UUID) -> Optional[User]:
        """Get a user by their ID."""
        result = await db.execute(
            select(User).filter(User.id == user_id)
        )
        return result.scalar_one_or_none()

    @staticmethod
    async def get_user_with_preferences(db: AsyncSession, user_id: UUID) -> dict:
        """Get user data along with their preferences (theme, personalization, etc.)."""
        user = await UserService.get_user_by_id(db, user_id)
        if not user:
            return None

        # Get theme preference
        theme_mode = await ThemeService.get_user_theme_mode(db, user_id)

        return {
            "user": user,
            "theme_preference": theme_mode
        }

    @staticmethod
    async def update_user_last_login(db: AsyncSession, user_id: UUID):
        """Update the last login time for a user."""
        user = await UserService.get_user_by_id(db, user_id)
        if user:
            from datetime import datetime
            user.last_login = datetime.utcnow()
            await db.commit()

    @staticmethod
    async def get_user_role(db: AsyncSession, user_id: UUID) -> Optional[str]:
        """Get the role of a user."""
        user = await UserService.get_user_by_id(db, user_id)
        return user.role if user else None

    @staticmethod
    async def is_admin_user(db: AsyncSession, user_id: UUID) -> bool:
        """Check if a user has admin role."""
        role = await UserService.get_user_role(db, user_id)
        return role == "admin"