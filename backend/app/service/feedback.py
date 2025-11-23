from sqlalchemy.orm import Session
from entities.table import Feedback, Picture
import uuid


def save_feedback(
    db: Session,
    picture_id: str,
    message: str,
    correct_label: str,
) -> Feedback:
    """Save user feedback for a picture classification and mark picture as having feedback.

    Args:
        db: SQLAlchemy Session
        picture_id: UUID of the picture
        message: User's feedback message
        correct_label: The correct label according to the user

    Returns:
        The created Feedback ORM instance
    """
    # Parse UUID
    pic_uuid = uuid.UUID(picture_id)

    # Create feedback record
    feedback = Feedback(
        picture_id=pic_uuid,
        message=message,
        correct_label=correct_label,
    )

    db.add(feedback)

    # Update the picture to mark that feedback has been given
    picture = db.query(Picture).filter(Picture.id == pic_uuid).first()
    if picture:
        picture.feedback_given = True  # type: ignore

    db.commit()
    db.refresh(feedback)

    return feedback
