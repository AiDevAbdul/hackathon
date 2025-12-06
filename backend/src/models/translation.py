from sqlalchemy import Column, String, DateTime, Text, Float
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid
from . import Base

class TranslationCache(Base):
    __tablename__ = "translation_cache"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    content_id = Column(String, nullable=False)  # Reference to textbook content
    target_language = Column(String, nullable=False)  # e.g., 'ur' for Urdu
    translated_content = Column(Text, nullable=False)
    confidence_score = Column(Float, nullable=True)  # Translation quality confidence (0.0-1.0)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    expires_at = Column(DateTime(timezone=True), nullable=False)  # Cache expiration

    def __repr__(self):
        return f"<TranslationCache(id={self.id}, content_id='{self.content_id}', target_language='{self.target_language}')>"