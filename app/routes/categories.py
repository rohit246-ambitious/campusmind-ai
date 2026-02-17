from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import SessionLocal
from app.models.category import Category
from app.schemas.category import CategoryCreate, CategoryResponse
from app.utils.dependencies import get_db, college_admin_only, get_current_user
from app.models.issue import Issue   



router = APIRouter(prefix="/categories", tags=["Categories"])


# -----------------------------
# Create Category (College Admin Only)
# -----------------------------
@router.post("/", response_model=CategoryResponse)
def create_category(
    category: CategoryCreate,
    db: Session = Depends(get_db),
    admin_user = Depends(college_admin_only)
):

    # Check duplicate category name inside same college
    existing = db.query(Category).filter(
        Category.name == category.name,
        Category.college_id == admin_user.college_id
    ).first()

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Category already exists for this college"
        )

    new_category = Category(
        name=category.name,
        college_id=admin_user.college_id
    )

    db.add(new_category)
    db.commit()
    db.refresh(new_category)

    return new_category


# -----------------------------
# List Categories (Tenant Safe)
# -----------------------------
@router.get("/", response_model=List[CategoryResponse])
def list_categories(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):

    categories = db.query(Category).filter(
        Category.college_id == current_user.college_id
    ).all()

    return categories


# -----------------------------
# Update Category (College Admin Only)
# -----------------------------
@router.put("/{category_id}", response_model=CategoryResponse)
def update_category(
    category_id: int,
    category: CategoryCreate,
    db: Session = Depends(get_db),
    admin_user = Depends(college_admin_only)
):

    db_category = db.query(Category).filter(
        Category.id == category_id,
        Category.college_id == admin_user.college_id
    ).first()

    if not db_category:
        raise HTTPException(status_code=404, detail="Category not found")

    # Prevent duplicate names
    duplicate = db.query(Category).filter(
        Category.name == category.name,
        Category.college_id == admin_user.college_id,
        Category.id != category_id
    ).first()

    if duplicate:
        raise HTTPException(
            status_code=400,
            detail="Another category with this name already exists"
        )

    db_category.name = category.name
    db.commit()
    db.refresh(db_category)

    return db_category


# -----------------------------
# Delete Category (College Admin Only)
# -----------------------------
@router.delete("/{category_id}")
def delete_category(
    category_id: int,
    db: Session = Depends(get_db),
    admin_user = Depends(college_admin_only)
):

    category = db.query(Category).filter(
        Category.id == category_id,
        Category.college_id == admin_user.college_id
    ).first()

    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    # 🚀 NEW VALIDATION
    issue_exists = db.query(Issue).filter(
        Issue.category_id == category_id
    ).first()

    if issue_exists:
        raise HTTPException(
            status_code=400,
            detail="Cannot delete category because issues exist under it"
        )

    db.delete(category)
    db.commit()

    return {"message": "Category deleted successfully"}

