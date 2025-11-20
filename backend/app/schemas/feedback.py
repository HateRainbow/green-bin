from pydantic import BaseModel, Field


class FeedbackCreate(BaseModel):
    user_id: int = Field(..., description="ID of the user providing feedback")
    message: str = Field(..., description="Feedback message from the user")
    yes_no: bool = Field(
        ..., description="Indicates if the image was classified correctly"
    )


class FeedbackResponse(BaseModel):
    id: int = Field(..., description="Unique identifier for the feedback")
    user_id: int = Field(..., description="ID of the user who provided the feedback")
    message: str = Field(..., description="Feedback message from the user")
    created_at: str = Field(..., description="Timestamp when the feedback was created")
