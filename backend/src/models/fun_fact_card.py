from sqlalchemy import Column, String, DateTime, Text, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
from . import Base

class FunFactCard(Base):
    __tablename__ = "fun_fact_cards"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    content_id = Column(String, ForeignKey("textbook_content.id"), nullable=False)  # Reference to textbook content
    title = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    category = Column(String, nullable=False)  # historical, technical, application
    difficulty_level = Column(String, nullable=False)  # beginner, intermediate, advanced
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)

    # Relationship
    content = relationship("TextbookContent", back_populates="fun_fact_cards")

    def __repr__(self):
        return f"<FunFactCard(id={self.id}, content_id='{self.content_id}', title='{self.title}')>"