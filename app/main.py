from fastapi import FastAPI
from app.database import engine
from app.models import user
from app.routes import auth
from app.routes import protected

app = FastAPI(title="CampusMind AI")

# create tables
user.Base.metadata.create_all(bind=engine)

# include routes
app.include_router(auth.router)
app.include_router(protected.router)

@app.get("/")
def home():
    return {"message": "CampusMind AI backend is running"}
