from fastapi import APIRouter
from pydantic import BaseModel
from app.services.scoring_service import score_answer

router = APIRouter()

class ScoringRequest(BaseModel):
    model_answer: str
    student_answer: str
    keywords: list[str]

@router.post("/")
async def get_score(request: ScoringRequest):
    score = score_answer(request.model_answer, request.student_answer, request.keywords)
    return {"score": score}
