from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, DateTime, func

# Create the base class for all models
Base = declarative_base()

# Import all models here to ensure they are registered with SQLAlchemy
from .user import User
from .user_progress import UserProgress
from .personalization import PersonalizationProfile
from .theme_preference import ThemePreference
from .fun_fact_card import FunFactCard
from .translation import TranslationCache
from .textbook_content import TextbookContent

__all__ = ["Base", "User", "UserProgress", "PersonalizationProfile", "ThemePreference", "FunFactCard", "TranslationCache", "TextbookContent"]