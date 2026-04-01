from pydantic import BaseModel
from typing import Optional


class CollegeCreate(BaseModel):
    name: str
    address: Optional[str]
    city: Optional[str]
    state: Optional[str]
    pincode: Optional[str]
    latitude: Optional[float]
    longitude: Optional[float]
    google_place_id: Optional[str]


class CollegeResponse(CollegeCreate):
    id: int
    is_active: bool

    class Config:
        from_attributes = True
