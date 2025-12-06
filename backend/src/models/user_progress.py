from sqlalchemy import Column, String, DateTime, Float, Integer, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import uuid
from . import Base

class UserProgress(Base):
    __tablename__ = "user_progress"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    content_id = Column(String, nullable=False)  # Reference to textbook content
    status = Column(String, nullable=False, default="not_started")  # not_started, in_progress, completed
    completion_percentage = Column(Float, nullable=False, default=0.0)  # 0.0 to 100.0
    time_spent_seconds = Column(Integer, nullable=True, default=0)
    last_accessed = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # Relationship
    user = relationship("User", back_populates="progress_records")

    def __repr__(self):
        return f"<UserProgress(id={self.id}, user_id={self.user_id}, content_id='{self.content_id}', status='{self.status}')>"