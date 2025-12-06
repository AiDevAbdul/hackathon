from typing import Optional, Dict, Any, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
import json
from uuid import UUID

from ..models.user import User
from ..models.personalization import PersonalizationProfile
from ..models.user_progress import UserProgress

class PersonalizationService:
    @staticmethod
    async def get_personalization_profile(db: AsyncSession, user_id: UUID) -> Optional[PersonalizationProfile]:
        """Get the personalization profile for a user."""
        result = await db.execute(
            select(PersonalizationProfile).filter(PersonalizationProfile.user_id == user_id)
        )
        return result.scalar_one_or_none()

    @staticmethod
    async def create_or_update_personalization_profile(
        db: AsyncSession,
        user_id: UUID,
        content_level_preference: Optional[str] = None,
        example_preference: Optional[str] = None,
        detail_preference: Optional[str] = None,
        learning_path: Optional[List[str]] = None
    ) -> PersonalizationProfile:
        """Create or update the personalization profile for a user."""
        # Try to get existing profile
        profile = await PersonalizationService.get_personalization_profile(db, user_id)

        if profile:
            # Update existing profile
            if content_level_preference is not None:
                profile.content_level_preference = content_level_preference
            if example_preference is not None:
                profile.example_preference = example_preference
            if detail_preference is not None:
                profile.detail_preference = detail_preference
            if learning_path is not None:
                profile.learning_path = json.dumps(learning_path)
        else:
            # Create new profile
            profile = PersonalizationProfile(
                user_id=user_id,
                content_level_preference=content_level_preference,
                example_preference=example_preference,
                detail_preference=detail_preference,
                learning_path=json.dumps(learning_path) if learning_path else "[]"
            )
            db.add(profile)

        await db.commit()
        await db.refresh(profile)
        return profile

    @staticmethod
    async def personalize_content(
        db: AsyncSession,
        user_id: UUID,
        content: str,
        content_metadata: Dict[str, Any] = None
    ) -> str:
        """Apply personalization to content based on user profile."""
        profile = await PersonalizationService.get_personalization_profile(db, user_id)

        if not profile:
            # Return content as is if no profile exists
            return content

        # Apply personalization based on user preferences
        personalized_content = content

        # Adjust content based on level preference
        if profile.content_level_preference:
            # This would involve more complex logic in a real implementation
            # For now, we'll just add a note about the level
            if profile.content_level_preference == "beginner":
                personalized_content = f"[Beginner Level] {content}"
            elif profile.content_level_preference == "advanced":
                personalized_content = f"[Advanced Level] {content}"

        # Modify examples based on preference
        if profile.example_preference == "practical":
            # Replace theoretical examples with practical ones
            # This is a simplified example - real implementation would be more sophisticated
            personalized_content = personalized_content.replace(
                "theoretical example",
                "practical example"
            )

        # Adjust detail level
        if profile.detail_preference == "concise":
            # This would involve summarization in a real implementation
            pass
        elif profile.detail_preference == "detailed":
            # This would involve expansion in a real implementation
            pass

        return personalized_content

    @staticmethod
    async def get_user_learning_path(db: AsyncSession, user_id: UUID) -> List[str]:
        """Get the user's customized learning path."""
        profile = await PersonalizationService.get_personalization_profile(db, user_id)

        if profile and profile.learning_path:
            try:
                return json.loads(profile.learning_path)
            except json.JSONDecodeError:
                return []

        return []

    @staticmethod
    async def adapt_content_for_user(
        db: AsyncSession,
        user_id: UUID,
        content: str,
        content_type: str = "textbook"
    ) -> Dict[str, Any]:
        """Adapt content for a specific user based on their preferences."""
        profile = await PersonalizationService.get_personalization_profile(db, user_id)

        result = {
            "original_content": content,
            "personalized_content": content,
            "adaptations_applied": [],
            "user_profile_used": bool(profile)
        }

        if profile:
            # Apply various adaptations based on profile
            adaptations = []

            if profile.content_level_preference:
                adaptations.append(f"level_adjusted_to_{profile.content_level_preference}")

            if profile.example_preference:
                adaptations.append(f"examples_adjusted_to_{profile.example_preference}")

            if profile.detail_preference:
                adaptations.append(f"detail_adjusted_to_{profile.detail_preference}")

            result["adaptations_applied"] = adaptations
            result["personalized_content"] = await PersonalizationService.personalize_content(
                db, user_id, content
            )

        return result