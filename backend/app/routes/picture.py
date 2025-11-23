from fastapi import APIRouter, File, UploadFile, HTTPException
from database.core import DbSession
from PIL import Image
from io import BytesIO
from AI.pipeline import get_pipe
from service.picture import save_picture
from entities.table import Picture
import base64
import uuid

picture_route = APIRouter()


@picture_route.post("/picture")
async def upload_picture(
    db: DbSession,
    file: UploadFile = File(...),
):
    if not file:
        return {"error": "No file uploaded"}
    content = await file.read()

    image = Image.open(BytesIO(content)).convert("RGB")
    pipe = get_pipe()
    result = pipe(image)[0]

    # Convert image to JPEG bytes for storage
    img_byte_arr = BytesIO()
    image.save(img_byte_arr, format="JPEG", quality=95)
    img_bytes = img_byte_arr.getvalue()

    # Save to database using service helper, return the persisted instance
    filename = file.filename or "unknown"
    picture = save_picture(
        db=db,
        filename=filename,
        image_bytes=img_bytes,  # Save as JPEG bytes, not raw pixels
        label=result["label"],
        confidence=float(result["score"]),
    )

    return {
        "id": str(picture.id),
        "confidence": str(result["score"]),
        "label": result["label"],
        "filename": file.filename,
    }


@picture_route.get("/picture/{picture_id}")
async def get_picture(picture_id: str, db: DbSession):
    """Retrieve a picture by ID including image data (base64 encoded)"""
    try:
        # Parse UUID
        pic_uuid = uuid.UUID(picture_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid picture ID format")

    # Query the database
    picture: Picture | None = db.query(Picture).filter(Picture.id == pic_uuid).first()

    if not picture:
        raise HTTPException(status_code=404, detail="Picture not found")

    # Extract values with explicit type hints to help Pylance
    image_data: bytes | None = picture.image  # type: ignore[assignment]
    confidence_value: float = float(picture.confidence)  # type: ignore[arg-type]
    created_timestamp = picture.created_at  # type: ignore[assignment]

    # Encode image bytes to base64 for JSON transmission
    image_base64 = base64.b64encode(image_data).decode("utf-8") if image_data else ""

    return {
        "id": str(picture.id),
        "filename": picture.filename,
        "label": picture.label,
        "confidence": confidence_value,
        "feedback_given": picture.feedback_given,
        "image": image_base64,  # Base64 encoded image
        "created_at": created_timestamp.isoformat()
        if created_timestamp is not None
        else None,
    }
