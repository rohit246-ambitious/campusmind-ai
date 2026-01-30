from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from sqlalchemy.orm import Session
import shutil
import os
from uuid import uuid4

from app.database import SessionLocal
from app.models.issue import Issue
from app.schemas.issue import IssueStatusUpdate
from app.utils.dependencies import get_current_user, admin_only
from app.utils.file_validation import validate_image
from app.utils.image_processor import process_and_save_image
from app.utils.security_scan import basic_image_safety_check
from app.utils.pagination import paginate
from app.services.issue_service import get_all_issues, search_issues


from app.schemas.issue import IssueResponse
from typing import List


router = APIRouter(prefix="/issues", tags=["Issues"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# -----------------------------
# Create Issue 
# -----------------------------
@router.post("/")
def create_issue(
    title: str = Form(...),
    description: str = Form(...),
    category_id: int = Form(...),
    latitude: float = Form(None),
    longitude: float = Form(None),
    image: UploadFile = File(None),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    image_path = None

    if image:
        validate_image(image) # Validate image

         # Step 2: basic security scan
        basic_image_safety_check(image)

        # Step 3: convert, resize & save
        image_path = process_and_save_image(image)
        os.makedirs("uploads", exist_ok=True)
        ext = image.filename.split(".")[-1]
        filename = f"{uuid4()}.{ext}"
        image_path = f"uploads/{filename}"

        with open(image_path, "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)

    new_issue = Issue(
        title=title,
        description=description,
        category_id=category_id,
        latitude=latitude,
        longitude=longitude,
        image_url=image_path,
        user_id=current_user.id
    )

    db.add(new_issue)
    db.commit()
    db.refresh(new_issue)

    return {"message": "Issue reported successfully", "issue_id": new_issue.id}


@router.get("/", response_model=List[IssueResponse])
def get_issues(
    db: Session = Depends(get_db),
    admin_user=Depends(admin_only)
):
    return get_all_issues(db)

@router.put("/{issue_id}/status")
def update_issue_status(
    issue_id: int,
    status_data: IssueStatusUpdate,
    db: Session = Depends(get_db),
    admin_user=Depends(admin_only)
):
    issue = db.query(Issue).filter(Issue.id == issue_id).first()

    if not issue:
        raise HTTPException(status_code=404, detail="Issue not found")

    issue.status = status_data.status
    db.commit()

    return {"message": "Status updated successfully"}


@router.get("/filter")
def filter_issues_by_category(
    category_id: int,
    db: Session = Depends(get_db),
    admin_user=Depends(admin_only)
):
    return db.query(Issue).filter(Issue.category_id == category_id).all()

@router.get("/paginated", response_model=List[IssueResponse])
def paginated_issues(
    page: int = 1,
    limit: int = 10,
    db: Session = Depends(get_db),
    admin_user=Depends(admin_only)
):
    query = db.query(Issue)
    return paginate(query, page, limit)

@router.get("/search", response_model=List[IssueResponse])
def search(
    keyword: str,
    db: Session = Depends(get_db),
    admin_user=Depends(admin_only)
):
    return search_issues(db, keyword)

