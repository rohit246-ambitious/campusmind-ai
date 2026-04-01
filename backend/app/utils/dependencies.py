from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models.user import User
from app.utils.jwt import SECRET_KEY, ALGORITHM


security = HTTPBearer()


# -----------------------------
# Database Dependency
# -----------------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# -----------------------------
# Get Current User
# -----------------------------
def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):

    try:
        token = credentials.credentials

        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")

        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")

        user = db.query(User).filter(User.id == user_id).first()

        if user is None:
            raise HTTPException(status_code=401, detail="User not found")

        return user

    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")


# -----------------------------
# Role Guards
# -----------------------------
def college_admin_only(current_user=Depends(get_current_user)):
    if current_user.role != "college_admin":
        raise HTTPException(status_code=403, detail="College Admin access only")
    return current_user


def super_admin_only(current_user=Depends(get_current_user)):
    if current_user.role != "super_admin":
        raise HTTPException(status_code=403, detail="Super Admin access only")
    return current_user


def admin_only(current_user=Depends(get_current_user)):
    if current_user.role not in ["college_admin", "super_admin"]:
        raise HTTPException(status_code=403, detail="Admin access only")
    return current_user
