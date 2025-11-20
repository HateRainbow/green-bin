from fastapi import APIRouter
from app.schemas.feedback import FeedbackCreate, FeedbackResponse


feedback_route = APIRouter(tags=["Feedback"])


@feedback_route.post(
    "/feedback", response_model=FeedbackResponse, summary="Submit user feedback"
)
async def submit_feedback(feedback: FeedbackCreate):
    mock_response = FeedbackResponse(
        id=1,
        user_id=feedback.user_id,
        message=feedback.message,
        created_at="2024-01-01T12:00:00Z",
    )
    return mock_response
