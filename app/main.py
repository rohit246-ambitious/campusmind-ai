from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.database import Base, engine
from app.utils.seed import seed_super_admin
from app.database import SessionLocal

# Import ALL models here so SQLAlchemy registers them
from app.models import User, College
from app.models.issue import Issue
from app.models.category import Category

# Import routes
from app.routes import auth
from app.routes import protected
from app.routes import issues
from app.routes import categories
from app.routes import dashboard
from app.routes import chatbot
from app.routes import college
from app.routes import admin_users



app = FastAPI(title="CampusMind AI")


# Create database tables
Base.metadata.create_all(bind=engine)

# Run Seeder
db = SessionLocal()
seed_super_admin(db)
db.close()

# Register routes
app.include_router(auth.router)
app.include_router(college.router)
app.include_router(categories.router)
app.include_router(admin_users.router)
app.include_router(protected.router)
app.include_router(issues.router)
app.include_router(dashboard.router)
app.include_router(chatbot.router)


# Static uploads folder
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")


@app.get("/")
def home():
    return {"message": "CampusMind AI backend is running"}
