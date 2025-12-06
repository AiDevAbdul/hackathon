from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid
from . import Base

class PersonalizationProfile(Base):
    __tablename__ = "personalization_profiles"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, unique=True)
    content_level_preference = Column(String, nullable=True)  # beginner, intermediate, advanced
    example_preference = Column(String, nullable=True)  # theoretical, practical
    detail_preference = Column(String, nullable=True)  # concise, detailed
    learning_path = Column(String, nullable=True)  # JSON string for learning path
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    def __repr__(self):
        return f"<PersonalizationProfile(id={self.id}, user_id={self.user_id})>"