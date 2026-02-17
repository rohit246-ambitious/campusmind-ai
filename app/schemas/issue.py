from pydantic import BaseModel
from typing import Optional

class IssueCreate(BaseModel):
    title: str
    description: str
    category_id: int
    image_url: Optional[str] = None

class IssueResponse(BaseModel):
    id: int
    title: str
    description: str
    status: str
    category_id: int
    image_url: Optional[str]

class IssueStatusUpdate(BaseModel):
    status: str

class Config:
    from_attributes = True
