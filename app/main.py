from fastapi import FastAPI
from app.database import engine
from app.models import user
from app.routes import auth
from app.routes import protected
from app.models import issue
from app.routes import issues
from app.models import category
from app.routes import categories
from fastapi.staticfiles import StaticFiles

app = FastAPI(title="CampusMind AI")

# create tables
user.Base.metadata.create_all(bind=engine)

# include routes
app.include_router(auth.router)
app.include_router(protected.router)
app.include_router(issues.router)
app.include_router(categories.router)

app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

@app.get("/")
def home():
    return {"message": "CampusMind AI backend is running"}
