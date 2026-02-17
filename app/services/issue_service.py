from sqlalchemy.orm import Session
from app.models.issue import Issue


def get_all_issues(db: Session):
    return db.query(Issue).all()

def search_issues(db, keyword, college_id):
    return db.query(Issue).filter(
        Issue.title.ilike(f"%{keyword}%"),
        Issue.college_id == college_id
    ).all()

