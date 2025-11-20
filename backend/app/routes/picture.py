from fastapi import APIRouter, File, UploadFile
from PIL import Image
from io import BytesIO
from schemas.picture import PictureResponse
from AI.pipeline import get_pipe

picture_route = APIRouter()


@picture_route.post("/picture")
async def upload_picture(file: UploadFile = File(...)):
    content = await file.read()

    image = Image.open(BytesIO(content)).convert("RGB")
    pipe = get_pipe()
    result = pipe(image)[0]
