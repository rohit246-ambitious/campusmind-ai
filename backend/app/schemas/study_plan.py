from pydantic import BaseModel
from typing import List


class StudyPlanRequest(BaseModel):
    message: str


class DayPlan(BaseModel):
    day: int
    task: str


class StudyPlanResponse(BaseModel):
    plan: List[DayPlan]