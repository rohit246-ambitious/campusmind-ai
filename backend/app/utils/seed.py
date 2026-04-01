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

def seed_colleges(db: Session):

    from app.models.college import College

    default_colleges = [
        "Engineering College",
        "Medical College",
        "Business School",
        "Arts College"
    ]

    for college_name in default_colleges:
        existing_college = db.query(College).filter(
            College.name == college_name
        ).first()

        if not existing_college:
            college = College(name=college_name)
            db.add(college)

    db.commit()
    print("✅ Default colleges seeded")

def seed_college_admin(db: Session, college_id: int):

    # Check if college admin already exists for this college
    existing_admin = db.query(User).filter(
        User.role == "college_admin",
        User.college_id == college_id
    ).first()

    if existing_admin:
        return  # Do nothing if exists

    # Create default college admin
    college_admin = User(
        name="College Admin",
        email=f"collegeadmin@{college_id}.com",
        password=hash_password("Admin@123"),
        role="college_admin",
        college_id=college_id
    )

    db.add(college_admin)
    db.commit()

    print(f"✅ Default College Admin created for College ID: {college_id}")



def seed_categories(db: Session, college_id: int):

    from app.models.category import Category

    default_categories = [
        "Infrastructure",
        "Academics",
        "Hostel",
        "Cafeteria",
        "Sports",
        "Library",
        "Transport"
    ]

    for cat_name in default_categories:
        existing_cat = db.query(Category).filter(
            Category.name == cat_name,
            Category.college_id == college_id
        ).first()

        if not existing_cat:
            category = Category(name=cat_name, college_id=college_id)
            db.add(category)

    db.commit()
    print(f"✅ Default categories seeded for College ID: {college_id}")
