from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from sqlalchemy.orm import Session
import os
from typing import List

from app.database import SessionLocal
from app.models.issue import Issue
from app.schemas.issue import IssueStatusUpdate, IssueResponse
from app.utils.dependencies import get_current_user, admin_only
from app.utils.file_validation import validate_image
from app.utils.image_processor import process_and_save_image
from app.utils.security_scan import basic_image_safety_check
from app.utils.pagination import paginate
from app.services.issue_service import search_issues


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
        validate_image(image)
        basic_image_safety_check(image)
        image_path = process_and_save_image(image)

    new_issue = Issue(
        title=title,
        description=description,
        category_id=category_id,
        latitude=latitude,
        longitude=longitude,
        image_url=image_path,
        user_id=current_user.id,
        college_id=current_user.college_id  # ⭐ MULTI TENANT
    )

    db.add(new_issue)
    db.commit()
    db.refresh(new_issue)

    return {"message": "Issue reported successfully", "issue_id": new_issue.id}


# -----------------------------
# Get Issues (Tenant Safe)
# -----------------------------
@router.get("/", response_model=List[IssueResponse])
def get_issues(
    db: Session = Depends(get_db),
    admin_user=Depends(admin_only)
):
    return db.query(Issue).filter(
        Issue.college_id == admin_user.college_id
    ).all()


# -----------------------------
# Update Status (Tenant Safe)
# -----------------------------
@router.put("/{issue_id}/status")
def update_issue_status(
    issue_id: int,
    status_data: IssueStatusUpdate,
    db: Session = Depends(get_db),
    admin_user=Depends(admin_only)
):

    issue = db.query(Issue).filter(
        Issue.id == issue_id,
        Issue.college_id == admin_user.college_id  # ⭐ SECURITY
    ).first()

    if not issue:
        raise HTTPException(status_code=404, detail="Issue not found")

    issue.status = status_data.status
    db.commit()

    return {"message": "Status updated successfully"}


# -----------------------------
# Filter By Category (Tenant Safe)
# -----------------------------
@router.get("/filter")
def filter_issues_by_category(
    category_id: int,
    db: Session = Depends(get_db),
    admin_user=Depends(admin_only)
):

    return db.query(Issue).filter(
        Issue.category_id == category_id,
        Issue.college_id == admin_user.college_id
    ).all()


# -----------------------------
# Paginated Issues (Tenant Safe)
# -----------------------------
@router.get("/paginated", response_model=List[IssueResponse])
def paginated_issues(
    page: int = 1,
    limit: int = 10,
    db: Session = Depends(get_db),
    admin_user=Depends(admin_only)
):

    query = db.query(Issue).filter(
        Issue.college_id == admin_user.college_id
    )

    return paginate(query, page, limit)


# -----------------------------
# Search Issues (Tenant Safe)
# -----------------------------
@router.get("/search", response_model=List[IssueResponse])
def search(
    keyword: str,
    db: Session = Depends(get_db),
    admin_user=Depends(admin_only)
):

    return search_issues(db, keyword, admin_user.college_id)


# -----------------------------
# student issue (Tenant Safe)
# -----------------------------
@router.get("/my-issues")
def my_issues(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return db.query(Issue).filter(
        Issue.user_id == current_user.id
    ).all()
