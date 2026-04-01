from fastapi import Depends, HTTPException
from app.utils.dependencies import get_current_user


def super_admin_only(user=Depends(get_current_user)):
    if user.role != "super_admin":
        raise HTTPException(status_code=403, detail="Super admin only")
    return user


def college_admin_only(user=Depends(get_current_user)):
    if user.role != "college_admin":
        raise HTTPException(status_code=403, detail="College admin only")
    return user
