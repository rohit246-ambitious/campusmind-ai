from sqlalchemy.orm import Session
from app.models.issue import Issue


def get_all_issues(db: Session):
    return db.query(Issue).all()

def search_issues(db: Session, keyword: str):
    return db.query(Issue).filter(
        Issue.title.ilike(f"%{keyword}%") |
        Issue.description.ilike(f"%{keyword}%")
    ).all()
