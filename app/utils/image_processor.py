import os
from uuid import uuid4
from PIL import Image
import pillow_heif
from fastapi import UploadFile, HTTPException

# Register HEIC support
pillow_heif.register_heif_opener()

MAX_WIDTH = 1920        # Full HD max width
MAX_HEIGHT = 1920
IMAGE_QUALITY = 80      # Good quality, smaller size

UPLOAD_DIR = "uploads"


def process_and_save_image(file: UploadFile) -> str:
    """
    1. Open image (HEIC / JPG / PNG)
    2. Convert to JPG
    3. Resize if too large
    4. Save optimized image
    """

    try:
        image = Image.open(file.file)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid image file")

    # Convert to RGB (required for JPG)
    if image.mode != "RGB":
        image = image.convert("RGB")

    # Resize if image is too large
    image.thumbnail((MAX_WIDTH, MAX_HEIGHT))

    # Ensure uploads folder exists
    os.makedirs(UPLOAD_DIR, exist_ok=True)

    filename = f"{uuid4()}.jpg"
    image_path = os.path.join(UPLOAD_DIR, filename)

    # Save optimized JPG
    image.save(image_path, "JPEG", quality=IMAGE_QUALITY, optimize=True)

    return image_path
