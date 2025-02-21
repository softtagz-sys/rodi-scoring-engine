from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.scoring_service import score_answer

router = APIRouter()

class ScoringRequest(BaseModel):
    model_answer: str
    student_answer: str
    keywords: list[str]
    correct_spelling: bool

@router.post("/")
async def get_score(request: ScoringRequest):
    try:
        score = score_answer(request.model_answer, request.student_answer, request.keywords, request.correct_spelling)
        return {"score": score}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

