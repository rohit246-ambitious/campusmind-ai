from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.schemas.study_plan import StudyPlanRequest, StudyPlanResponse
from app.services.study_planner_service import generate_study_plan
from app.utils.dependencies import get_current_user, get_db


router = APIRouter(prefix="/study-plan", tags=["Study Planner"])


@router.post("/generate", response_model=StudyPlanResponse)
def create_study_plan(
    data: StudyPlanRequest,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):

    result = generate_study_plan(data.message)

    return result