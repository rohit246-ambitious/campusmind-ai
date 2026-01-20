from fastapi import APIRouter, Depends
from app.utils.dependencies import get_current_user, admin_only

router = APIRouter(prefix="/protected", tags=["Protected"])

@router.get("/me")
def read_profile(current_user=Depends(get_current_user)):
    return {
        "id": current_user.id,
        "name": current_user.name,
        "email": current_user.email,
        "role": current_user.role
    }

@router.get("/admin")
def admin_dashboard(admin_user=Depends(admin_only)):
    return {"message": "Welcome admin"}
