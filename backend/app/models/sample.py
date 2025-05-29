import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, DateTime, Enum, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base, relationship
import enum

Base = declarative_base()

class SampleStatus(str, enum.Enum):
    pending = "pending"
    in_progress = "in-progress"
    complete = "complete"

class Sample(Base):
    __tablename__ = "samples"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    sample_id = Column(String(100), unique=True, nullable=False)
    source = Column(String(100), nullable=False)
    status = Column(Enum(SampleStatus), nullable=False, default=SampleStatus.pending)
    type = Column(String(100), nullable=False)

    assigned_user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)

    date_collected = Column(DateTime, nullable=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)

    # If user model exists
    # assigned_user = relationship("User", back_populates="samples")