from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from typing import Optional
import logging
from ..services.personalization_service import PersonalizationService
from ..models.user import User
from ..utils.logging import app_logger
from ..config.settings import settings


class PersonalizationMiddleware:
    def __init__(self, personalization_service: PersonalizationService):
        self.personalization_service = personalization_service

    async def __call__(self, request: Request, call_next):
        # Get user from request state (should be set by auth middleware)
        user: User = getattr(request.state, 'user', None)

        if user:
            try:
                # Get user's personalization profile
                profile = await self.personalization_service.get_profile_by_user_id(
                    user.id
                )
                if profile:
                    # Add personalization context to request state
                    request.state.personalization_context = {
                        'user_background_software': user.background_software,
                        'user_background_hardware': user.background_hardware,
                        'content_level_preference': profile.content_level_preference,
                        'example_preference': profile.example_preference,
                        'detail_preference': profile.detail_preference
                    }
                else:
                    # Set default personalization context
                    request.state.personalization_context = {
                        'user_background_software': user.background_software,
                        'user_background_hardware': user.background_hardware,
                        'content_level_preference': 'intermediate',
                        'example_preference': 'balanced',
                        'detail_preference': 'balanced'
                    }
            except Exception as e:
                app_logger.error(f"Error getting personalization profile: {e}")
                request.state.personalization_context = None
        else:
            request.state.personalization_context = None

        response = await call_next(request)
        return response


def add_personalization_middleware(app, personalization_service: PersonalizationService):
    """Function to add personalization middleware to FastAPI app"""
    @app.middleware("http")
    async def personalization_middleware(request: Request, call_next):
        middleware = PersonalizationMiddleware(personalization_service)
        return await middleware(request, call_next)