from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models.user import User
from app.models.college import College
from app.utils.security import hash_password
from app.utils.dependencies import get_current_user


router = APIRouter(prefix="/admin-users", tags=["Admin Users"])


# Database Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# -----------------------------------------
# Super Admin → Create College Admin
# -----------------------------------------
@router.post("/college-admin")
def create_college_admin(
    name: str,
    email: str,
    password: str,
    college_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):

    # Check permission
    if current_user.role != "super_admin":
        raise HTTPException(status_code=403, detail="Only Super Admin allowed")

    # Validate college exists
    college = db.query(College).filter(College.id == college_id).first()

    if not college:
        raise HTTPException(status_code=404, detail="College not found")

    # Check email uniqueness
    existing = db.query(User).filter(User.email == email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Create College Admin
    new_admin = User(
        name=name,
        email=email,
        password=hash_password(password),
        role="college_admin",
        college_id=college_id
    )

    db.add(new_admin)
    db.commit()
    db.refresh(new_admin)

    return {
        "message": "College admin created successfully",
        "admin_id": new_admin.id
    }


# -----------------------------------------
# College Admin → Create College Users
# -----------------------------------------
@router.post("/college-user")
def create_college_user(
    name: str,
    email: str,
    password: str,
    role: str,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):

    # Only College Admin allowed
    if current_user.role != "college_admin":
        raise HTTPException(status_code=403, detail="Only College Admin allowed")

    # Restrict allowed roles
    allowed_roles = ["student", "teacher", "staff"]

    if role not in allowed_roles:
        raise HTTPException(
            status_code=400,
            detail=f"Role must be one of {allowed_roles}"
        )

    # Check duplicate email
    existing = db.query(User).filter(User.email == email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Create new user under SAME college
    new_user = User(
        name=name,
        email=email,
        password=hash_password(password),
        role=role,
        college_id=current_user.college_id   # ⭐ auto assign tenant
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "message": f"{role} created successfully",
        "user_id": new_user.id
    }
