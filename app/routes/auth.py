from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models.user import User
from app.schemas.user import UserLogin
from app.utils.security import verify_password
from app.utils.jwt import create_access_token


router = APIRouter(prefix="/auth", tags=["Authentication"])


# Database Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# -----------------------------------------
# LOGIN ENDPOINT
# -----------------------------------------
@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):

    # Find user by email
    db_user = db.query(User).filter(User.email == user.email).first()

    # Validate credentials
    if not db_user or not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # Create multi-tenant JWT token
    access_token = create_access_token(db_user)

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "role": db_user.role,
        "college_id": db_user.college_id
    }
