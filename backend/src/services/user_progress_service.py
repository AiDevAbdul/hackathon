from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from uuid import UUID

from ..models.user import User
from ..models.user_progress import UserProgress

class UserProgressService:
    @staticmethod
    async def get_user_progress(db: AsyncSession, user_id: UUID, content_id: str) -> Optional[UserProgress]:
        """Get user progress for a specific content."""
        result = await db.execute(
            select(UserProgress)
            .filter(UserProgress.user_id == user_id)
            .filter(UserProgress.content_id == content_id)
        )
        return result.scalar_one_or_none()

    @staticmethod
    async def create_or_update_progress(
        db: AsyncSession,
        user_id: UUID,
        content_id: str,
        status: str = "not_started",
        completion_percentage: float = 0.0,
        time_spent_seconds: Optional[int] = None,
        notes: Optional[str] = None
    ) -> UserProgress:
        """Create or update user progress for a specific content."""
        # Validate status
        valid_statuses = ["not_started", "in_progress", "completed"]
        if status not in valid_statuses:
            raise ValueError(f"Invalid status. Must be one of: {valid_statuses}")

        # Validate completion percentage
        if completion_percentage < 0 or completion_percentage > 100:
            raise ValueError("Completion percentage must be between 0 and 100")

        # Try to get existing progress record
        progress = await UserProgressService.get_user_progress(db, user_id, content_id)

        if progress:
            # Update existing progress
            progress.status = status
            progress.completion_percentage = completion_percentage
            if time_spent_seconds is not None:
                progress.time_spent_seconds = time_spent_seconds
            if notes is not None:
                progress.notes = notes
        else:
            # Create new progress record
            progress = UserProgress(
                user_id=user_id,
                content_id=content_id,
                status=status,
                completion_percentage=completion_percentage,
                time_spent_seconds=time_spent_seconds or 0,
                notes=notes
            )
            db.add(progress)

        await db.commit()
        await db.refresh(progress)
        return progress

    @staticmethod
    async def get_user_content_progress(db: AsyncSession, user_id: UUID, content_ids: list) -> list:
        """Get progress for multiple contents for a user."""
        result = await db.execute(
            select(UserProgress)
            .filter(UserProgress.user_id == user_id)
            .filter(UserProgress.content_id.in_(content_ids))
        )
        return result.scalars().all()

    @staticmethod
    async def mark_content_completed(db: AsyncSession, user_id: UUID, content_id: str) -> UserProgress:
        """Mark a content as completed with 100% completion."""
        return await UserProgressService.create_or_update_progress(
            db, user_id, content_id, status="completed", completion_percentage=100.0
        )

    @staticmethod
    async def mark_content_in_progress(db: AsyncSession, user_id: UUID, content_id: str) -> UserProgress:
        """Mark a content as in progress."""
        return await UserProgressService.create_or_update_progress(
            db, user_id, content_id, status="in_progress"
        )

    @staticmethod
    async def get_user_completed_contents(db: AsyncSession, user_id: UUID) -> list:
        """Get all contents completed by a user."""
        result = await db.execute(
            select(UserProgress)
            .filter(UserProgress.user_id == user_id)
            .filter(UserProgress.status == "completed")
        )
        return result.scalars().all()

    @staticmethod
    async def get_user_progress_summary(db: AsyncSession, user_id: UUID) -> dict:
        """Get a summary of user progress."""
        all_progress = await db.execute(
            select(UserProgress).filter(UserProgress.user_id == user_id)
        )
        progress_list = all_progress.scalars().all()

        total_contents = len(progress_list)
        completed_contents = len([p for p in progress_list if p.status == "completed"])
        in_progress_contents = len([p for p in progress_list if p.status == "in_progress"])

        total_time_spent = sum(p.time_spent_seconds or 0 for p in progress_list)

        if total_contents > 0:
            avg_completion = sum(p.completion_percentage for p in progress_list) / total_contents
        else:
            avg_completion = 0.0

        return {
            "total_contents": total_contents,
            "completed_contents": completed_contents,
            "in_progress_contents": in_progress_contents,
            "not_started_contents": total_contents - completed_contents - in_progress_contents,
            "average_completion_percentage": avg_completion,
            "total_time_spent_seconds": total_time_spent
        }