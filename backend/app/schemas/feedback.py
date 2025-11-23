from pydantic import BaseModel, Field


class FeedbackCreate(BaseModel):
    is_correct: bool = Field(..., description="Is the AI classification correct?")
    message: str = Field(
        ..., description="User feedback message (required if incorrect)"
    )
    correct_label: str = Field(
        ..., description="Correct label if classification was wrong"
    )


class FeedbackResponse(BaseModel):
    id: int = Field(..., description="Unique identifier for the feedback")
    picture_id: str = Field(..., description="ID of the picture this feedback is for")
    message: str = Field(..., description="Feedback message from the user")
    correct_label: str = Field(..., description="The correct label provided by user")
    created_at: str = Field(..., description="Timestamp when the feedback was created")
