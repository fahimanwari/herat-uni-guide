from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import get_db
from .service import QuizService
from .schemas import QuestionSchema, QuizMatch, ScoreRequest

router = APIRouter(prefix="/quiz", tags=["quiz"])


@router.get("/questions", response_model=list[QuestionSchema])
async def list_questions(db: AsyncSession = Depends(get_db)):
    return await QuizService(db).get_questions()


@router.post("/score", response_model=list[QuizMatch])
async def score_quiz(payload: ScoreRequest, db: AsyncSession = Depends(get_db)):
    return await QuizService(db).score(payload.selected_option_ids)
