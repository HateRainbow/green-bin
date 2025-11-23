from pydantic import BaseModel, Field


class PictureResponse(BaseModel):
    id: int = Field(..., description="Unique identifier for the picture")
    filename: str | None = Field(..., description="Name of the uploaded picture file")
    label: str = Field(..., description="Predicted label for the picture")
    confidence: str = Field(..., description="Confidence score of the prediction")
