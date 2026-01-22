from pydantic import BaseModel

class IssueCreate(BaseModel):
    title: str
    description: str

class IssueResponse(BaseModel):
    id: int
    title: str
    description: str
    status: str
    user_id: int
