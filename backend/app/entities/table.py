import uuid

from database.core import Base
from sqlalchemy import (
    BINARY,
    DECIMAL,
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func


class Picture(Base):
    __tablename__ = "pictures"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    filename = Column(String, unique=False, nullable=False, index=True)
    label = Column(String, index=True, nullable=False)
    confidence = Column(DECIMAL(4, 2), nullable=False)
    feedback_given = Column(Boolean, default=False)
    image = Column(BINARY, nullable=False)
    created_at = Column(DateTime, server_default=func.now())


class Feedback(Base):
    __tablename__ = "feedbacks"

    id = Column(Integer, primary_key=True, index=True)
    picture_id = Column(Integer, ForeignKey("pictures.id"), nullable=False)
    correct_label = Column(Boolean, index=False, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    message = Column(String, nullable=False)
    correct_label = Column(String, nullable=False)
