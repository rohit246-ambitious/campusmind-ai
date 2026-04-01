from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models.college import College
from app.schemas.college import CollegeCreate, CollegeResponse
from app.utils.role_guards import super_admin_only

router = APIRouter(prefix="/colleges", tags=["Colleges"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=CollegeResponse)
def create_college(
    data: CollegeCreate,
    db: Session = Depends(get_db),
    admin=Depends(super_admin_only)
):
    college = College(**data.dict())
    db.add(college)
    db.commit()
    db.refresh(college)
    return college


@router.get("/", response_model=list[CollegeResponse])
def get_all_colleges(
    db: Session = Depends(get_db),
    admin=Depends(super_admin_only)
):
    return db.query(College).all()
