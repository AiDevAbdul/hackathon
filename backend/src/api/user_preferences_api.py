from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from typing import List, Optional

from ..database import get_db
from ..models.user import User
from ..api.auth_api import get_current_user

router = APIRouter()

class ThemePreferenceRequest(BaseModel):
    theme_mode: str  # light, dark, system

class ThemePreferenceResponse(BaseModel):
    id: str
    user_id: str
    theme_mode: str
    created_at: str
    updated_at: str

class PersonalizationProfileRequest(BaseModel):
    content_level_preference: Optional[str] = None  # beginner, intermediate, advanced
    example_preference: Optional[str] = None  # theoretical, practical
    detail_preference: Optional[str] = None  # concise, detailed
    learning_path: Optional[List[str]] = []

class PersonalizationProfileResponse(BaseModel):
    id: str
    user_id: str
    content_level_preference: Optional[str] = None
    example_preference: Optional[str] = None
    detail_preference: Optional[str] = None
    learning_path: List[str] = []
    created_at: str
    updated_at: str

@router.get("/theme", response_model=ThemePreferenceResponse)
async def get_theme_preference(
    current_user: User = Depends(get_current_user)
):
    """Get user's theme preference."""
    # This would typically fetch from a database
    # For now, return a default response
    from datetime import datetime
    return ThemePreferenceResponse(
        id="default_theme_pref_id",
        user_id=str(current_user.id),
        theme_mode="system",
        created_at=datetime.utcnow().isoformat(),
        updated_at=datetime.utcnow().isoformat()
    )

@router.put("/theme", response_model=ThemePreferenceResponse)
async def update_theme_preference(
    request: ThemePreferenceRequest,
    current_user: User = Depends(get_current_user)
):
    """Update user's theme preference."""
    # Validate theme mode
    valid_modes = ["light", "dark", "system"]
    if request.theme_mode not in valid_modes:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid theme mode. Must be one of: {valid_modes}"
        )

    # This would typically update the database
    # For now, return the updated preference
    from datetime import datetime
    return ThemePreferenceResponse(
        id="default_theme_pref_id",
        user_id=str(current_user.id),
        theme_mode=request.theme_mode,
        created_at=datetime.utcnow().isoformat(),
        updated_at=datetime.utcnow().isoformat()
    )

@router.get("/personalization", response_model=PersonalizationProfileResponse)
async def get_personalization_profile(
    current_user: User = Depends(get_current_user)
):
    """Get user's personalization profile."""
    # This would typically fetch from a database
    # For now, return a default response
    from datetime import datetime
    return PersonalizationProfileResponse(
        id="default_personalization_id",
        user_id=str(current_user.id),
        content_level_preference="intermediate",
        example_preference="practical",
        detail_preference="concise",
        learning_path=[],
        created_at=datetime.utcnow().isoformat(),
        updated_at=datetime.utcnow().isoformat()
    )

@router.put("/personalization", response_model=PersonalizationProfileResponse)
async def update_personalization_profile(
    request: PersonalizationProfileRequest,
    current_user: User = Depends(get_current_user)
):
    """Update user's personalization profile."""
    # This would typically update the database
    # For now, return the updated profile
    from datetime import datetime
    return PersonalizationProfileResponse(
        id="default_personalization_id",
        user_id=str(current_user.id),
        content_level_preference=request.content_level_preference,
        example_preference=request.example_preference,
        detail_preference=request.detail_preference,
        learning_path=request.learning_path or [],
        created_at=datetime.utcnow().isoformat(),
        updated_at=datetime.utcnow().isoformat()
    )