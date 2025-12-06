from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from uuid import UUID

from ..models.user import User
from ..models.theme_preference import ThemePreference

class ThemeService:
    @staticmethod
    async def get_theme_preference(db: AsyncSession, user_id: UUID) -> Optional[ThemePreference]:
        """Get the theme preference for a user."""
        result = await db.execute(
            select(ThemePreference).filter(ThemePreference.user_id == user_id)
        )
        return result.scalar_one_or_none()

    @staticmethod
    async def create_or_update_theme_preference(
        db: AsyncSession,
        user_id: UUID,
        theme_mode: str
    ) -> ThemePreference:
        """Create or update the theme preference for a user."""
        # Validate theme mode
        valid_modes = ["light", "dark", "system"]
        if theme_mode not in valid_modes:
            raise ValueError(f"Invalid theme mode. Must be one of: {valid_modes}")

        # Try to get existing preference
        preference = await ThemeService.get_theme_preference(db, user_id)

        if preference:
            # Update existing preference
            preference.theme_mode = theme_mode
        else:
            # Create new preference
            preference = ThemePreference(
                user_id=user_id,
                theme_mode=theme_mode
            )
            db.add(preference)

        await db.commit()
        await db.refresh(preference)
        return preference

    @staticmethod
    async def get_user_theme_mode(db: AsyncSession, user_id: UUID) -> str:
        """Get the theme mode for a user, defaulting to 'system' if not set."""
        preference = await ThemeService.get_theme_preference(db, user_id)

        if preference:
            return preference.theme_mode
        else:
            # Return default theme mode
            return "system"

    @staticmethod
    async def reset_theme_preference(db: AsyncSession, user_id: UUID) -> ThemePreference:
        """Reset the user's theme preference to default."""
        return await ThemeService.create_or_update_theme_preference(db, user_id, "system")