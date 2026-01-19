from fastapi import FastAPI

app = FastAPI(title="CampusMind AI")

@app.get("/")
def home():
    return {"message": "CampusMind AI backend is running"}
