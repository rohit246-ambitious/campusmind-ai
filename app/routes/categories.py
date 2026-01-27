from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models.category import Category
from app.schemas.category import CategoryCreate
from app.utils.dependencies import admin_only

router = APIRouter(prefix="/categories", tags=["Categories"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Create category (admin only)
@router.post("/")
def create_category(
    category: CategoryCreate,
    db: Session = Depends(get_db),
    admin_user = Depends(admin_only)
):
    new_cat = Category(name=category.name)
    db.add(new_cat)
    db.commit()
    db.refresh(new_cat)

    return {"message": "Category created", "id": new_cat.id}


# List categories (public)
@router.get("/")
def list_categories(db: Session = Depends(get_db)):
    Categories = db.query(Category).all()
    if not Categories:
        return {"message": "No categories found"}
    return Categories

# Delete category (admin only)
@router.delete("/{category_id}")
def delete_category(
    category_id: int,
    db: Session = Depends(get_db),
    admin_user = Depends(admin_only)
):
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        return {"message": "Category not found"}
    db.delete(category)
    db.commit()
    return {"message": "Category deleted"}

# Update category (admin only)
@router.put("/{category_id}")
def update_category(
    category_id: int,
    category: CategoryCreate,
    db: Session = Depends(get_db),
    admin_user = Depends(admin_only)
):
    db_category = db.query(Category).filter(Category.id == category_id).first()
    if not db_category:
        return {"message": "Category not found"}
    db_category.name = category.name
    db.commit()
    db.refresh(db_category)
    return {"message": "Category updated"}