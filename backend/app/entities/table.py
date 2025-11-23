import uuid

from database.core import Base
from sqlalchemy import (
    DECIMAL,
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    LargeBinary,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func


class Picture(Base):
    """
    Database model representing uploaded pictures with classification results.
    This table stores images along with their AI-generated labels and confidence scores.
    It also tracks whether human feedback has been provided for the classification.

    Attributes:
        id (UUID): Primary key, automatically generated UUID for each picture
        filename (str): Original filename of the uploaded image, indexed for faster queries
        label (str): AI-generated classification label for the image content, indexed
        confidence (Decimal): Classification confidence score (0.00 to 99.99)
        feedback_given (bool): Flag indicating if human feedback has been provided, defaults to False
        image (bytes): Binary data of the actual image file
        created_at (datetime): Timestamp when the record was created, auto-generated
    """

    __tablename__ = "pictures"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    filename = Column(String, unique=False, nullable=False, index=True)
    label = Column(String, index=True, nullable=False)
    confidence = Column(DECIMAL(4, 2), nullable=False)
    feedback_given = Column(Boolean, default=False)
    image = Column(LargeBinary, nullable=False)
    created_at = Column(DateTime, server_default=func.now())


class Feedback(Base):
    """
    Feedback table for storing user feedback on picture classifications.
    This table captures user feedback about the correctness of AI-generated labels
    for pictures, allowing the system to learn from user corrections and improve
    classification accuracy over time.

    Attributes:
        id (int): Primary key, unique identifier for each feedback entry
        picture_id (UUID): Foreign key reference to pictures.id, links feedback to specific picture
        correct_label (Boolean): Indicates whether the AI-generated label was correct
        created_at (DateTime): Timestamp when the feedback was created, defaults to current time
        message (str): User's feedback message or comments about the classification
        correct_label (str): The correct label as provided by the user

    Note:
        There appears to be a duplicate 'correct_label' column definition in the current schema.
        Consider using different names like 'is_correct' (Boolean) and 'user_provided_label' (String)
        to distinguish between the correctness indicator and the actual correct label.
    """

    __tablename__ = "feedbacks"

    id = Column(Integer, primary_key=True, index=True)
    picture_id = Column(UUID(as_uuid=True), ForeignKey("pictures.id"), nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    message = Column(String, nullable=False)
    correct_label = Column(String, nullable=False)
