from pydantic import BaseModel

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
    user_id: int

class IssueStatusUpdate(BaseModel):
    status: str


