from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from sqlalchemy.orm import Session
import shutil
import os
from uuid import uuid4

from app.database import SessionLocal
from app.models.issue import Issue
from app.schemas.issue import IssueStatusUpdate
from app.utils.dependencies import get_current_user, admin_only

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


@router.get("/")
def get_all_issues(
    db: Session = Depends(get_db),
    admin_user=Depends(admin_only)
):
    return db.query(Issue).all()


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
