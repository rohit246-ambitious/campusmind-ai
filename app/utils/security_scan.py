from fastapi import UploadFile, HTTPException

def basic_image_safety_check(file: UploadFile):
    # Read first few bytes (magic numbers)
    header = file.file.read(10)
    file.file.seek(0)

    allowed_headers = [
        b"\xff\xd8\xff",   # JPEG
        b"\x89PNG",        # PNG
        b"ftypheic",       # HEIC
        b"ftypheif"
    ]

    if not any(h in header for h in allowed_headers):
        raise HTTPException(
            status_code=400,
            detail="Suspicious or unsupported image file"
        )
