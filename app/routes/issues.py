from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models.issue import Issue
from app.schemas.issue import IssueCreate
from app.utils.dependencies import get_current_user, admin_only

router = APIRouter(prefix="/issues", tags=["Issues"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/")
def create_issue(
    issue: IssueCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    new_issue = Issue(
        title=issue.title,
        description=issue.description,
        user_id=current_user.id
    )

    db.add(new_issue)
    db.commit()
    db.refresh(new_issue)

    return {"message": "Issue reported successfully", "issue_id": new_issue.id}

@router.get("/")
def get_all_issues(
    db: Session = Depends(get_db),
    admin_user = Depends(admin_only)
):
    issues = db.query(Issue).all()
    return issues
