from sqlalchemy import Column, String, Integer, Text, Boolean, DateTime
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid

from . import Base


class TextbookContent(Base):
    __tablename__ = "textbook_content"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String, nullable=False)
    slug = Column(String, unique=True, nullable=False, index=True)
    content = Column(Text, nullable=False)
    content_ur = Column(Text)  # Urdu translation
    chapter_number = Column(Integer, nullable=False)
    section_number = Column(Integer)
    level = Column(String(20), nullable=False)  # beginner, intermediate, advanced
    prerequisites = Column(JSONB)  # JSON array of prerequisites
    learning_objectives = Column(JSONB)  # JSON array of learning objectives
    is_published = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    user_progress = relationship("UserProgress", back_populates="content")
    fun_fact_cards = relationship("FunFactCard", back_populates="content", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<TextbookContent(id={self.id}, title={self.title}, slug={self.slug})>"