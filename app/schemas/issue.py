from pydantic import BaseModel
from typing import Optional

class IssueCreate(BaseModel):
    title: str
    description: str
    category_id: int
    latitude: float | None = None
    longitude: float | None = None

class IssueResponse(BaseModel):
    id: int
    title: str
    description: str
    status: str
    category_id: int
    image_url: Optional[str]
    latitude: Optional[float]
    longitude: Optional[float]

class IssueStatusUpdate(BaseModel):
    status: str

class Config:
    orm_mode = True
