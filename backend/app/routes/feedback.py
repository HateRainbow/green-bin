from fastapi import APIRouter, HTTPException
from schemas.feedback import FeedbackCreate, FeedbackResponse
from database.core import DbSession
from service.feedback import save_feedback
from entities.table import Picture
import uuid


feedback_route = APIRouter(tags=["Feedback"])


@feedback_route.post(
    "/feedback/{picture_id}",
    response_model=FeedbackResponse,
    summary="Submit user feedback for a picture classification",
)
async def submit_feedback(
    picture_id: str,
    feedback: FeedbackCreate,
    db: DbSession,
):
    """
    Submit feedback for a picture classification.

    - If is_correct=True, just saves confirmation feedback
    - If is_correct=False, saves the correct label and message
    - Updates the picture's feedback_given flag
    """
    try:
        # Validate UUID
        pic_uuid = uuid.UUID(picture_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid picture ID format")

    # Check if picture exists
    picture = db.query(Picture).filter(Picture.id == pic_uuid).first()
    if not picture:
        raise HTTPException(status_code=404, detail="Picture not found")

    # Determine message and correct label based on feedback
    if feedback.is_correct:
        message = feedback.message or "Classification confirmed as correct"
        correct_label = str(picture.label)  # Keep the AI's label
    else:
        if not feedback.correct_label:
            raise HTTPException(
                status_code=400,
                detail="correct_label is required when is_correct=False",
            )
        message = feedback.message
        correct_label = feedback.correct_label

    # Save feedback using service
    feedback_record = save_feedback(
        db=db,
        picture_id=picture_id,
        message=message,
        correct_label=correct_label,
    )

    return FeedbackResponse(
        id=feedback_record.id,  # type: ignore
        picture_id=str(feedback_record.picture_id),
        message=feedback_record.message,  # type: ignore
        correct_label=feedback_record.correct_label,  # type: ignore
        created_at=feedback_record.created_at.isoformat()
        if feedback_record.created_at is not None
        else "",  # type: ignore
    )
