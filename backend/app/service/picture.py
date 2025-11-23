from sqlalchemy.orm import Session
from entities.table import Picture


def save_picture(
    db: Session,
    filename: str,
    image_bytes: bytes,
    label: str,
    confidence: float,
) -> Picture:
    """Save an image and its classification into the database.

    Args:
        db: SQLAlchemy Session
        filename: original filename
        image_bytes: raw image bytes to store
        label: classification label
        confidence: classification confidence (0-100 scale expected)

    Returns:
        The created Picture ORM instance (committed and refreshed).
    """

    picture = Picture(
        filename=filename,
        image=image_bytes,
        label=label,
        confidence=confidence,
    )

    db.add(picture)
    db.commit()
    db.refresh(picture)

    return picture


def upload_picture_deprecated(image: bytes, db: Session):
    """Backward-compatible helper (kept for older callers).

    This mirrors the previous simple upload behaviour but returns the created
    Picture instance instead of a dict.
    """
    return save_picture(
        db=db, filename="unknown", image_bytes=image, label="unknown", confidence=0.0
    )
