from sqlalchemy.orm import Session
from app.models.user import User
from app.utils.security import hash_password


def seed_super_admin(db: Session):

    # Check if super admin already exists
    existing_admin = db.query(User).filter(User.role == "super_admin").first()

    if existing_admin:
        return  # Do nothing if exists

    # Create default super admin
    super_admin = User(
        name="Super Admin",
        email="superadmin@campusmind.com",
        password=hash_password("Admin@123"),
        role="super_admin",
        college_id=None
    )

    db.add(super_admin)
    db.commit()

    print("✅ Default Super Admin created")
