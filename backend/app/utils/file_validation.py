from fastapi import UploadFile, HTTPException

ALLOWED_TYPES = ["image/jpeg", "image/png", "image/webp", "image/heic", "image/heif"]
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB


def validate_image(file: UploadFile):
    # 1. Check content type
    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(
            status_code=400,
            detail="Only JPG, PNG, WEBP, HEIC, HEIF images are allowed"
        )

    # 2. Check file size
    file.file.seek(0, 2)  # move cursor to end
    size = file.file.tell()
    file.file.seek(0)     # reset cursor

    if size > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=400,
            detail="Image size must be less than 10MB"
        )
