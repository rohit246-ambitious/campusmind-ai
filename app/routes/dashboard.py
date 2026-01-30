from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.database import SessionLocal
from app.models.issue import Issue
from app.utils.dependencies import admin_only

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/stats")
def dashboard_stats(
    db: Session = Depends(get_db),
    admin_user=Depends(admin_only)
):
    total = db.query(func.count(Issue.id)).scalar()
    open_count = db.query(Issue).filter(Issue.status == "open").count()
    resolved = db.query(Issue).filter(Issue.status == "resolved").count()

    return {
        "total_issues": total,
        "open": open_count,
        "resolved": resolved
    }
