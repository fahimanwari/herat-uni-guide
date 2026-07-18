import uuid
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import get_db
from app.core.security import get_current_admin
from .service import QuizService
from .schemas import QuestionSchema, QuizMatch, ScoreRequest

router = APIRouter(prefix="/quiz", tags=["quiz"])


# --- Public ---

@router.get("/questions", response_model=list[QuestionSchema])
async def list_questions(db: AsyncSession = Depends(get_db)):
    return await QuizService(db).get_questions()


@router.post("/score", response_model=list[QuizMatch])
async def score_quiz(payload: ScoreRequest, db: AsyncSession = Depends(get_db)):
    return await QuizService(db).score(payload.selected_option_ids)


# --- Admin CRUD ---

@router.post("/questions")
async def create_question(
    payload: QuestionSchema,
    db: AsyncSession = Depends(get_db),
    admin=Depends(get_current_admin),
):
    return await QuizService(db).create_question(payload)


@router.patch("/questions/{question_id}")
async def update_question(
    question_id: uuid.UUID,
    payload: QuestionSchema,
    db: AsyncSession = Depends(get_db),
    admin=Depends(get_current_admin),
):
    return await QuizService(db).update_question(question_id, payload)


@router.delete("/questions/{question_id}")
async def delete_question(
    question_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    admin=Depends(get_current_admin),
):
    return await QuizService(db).delete_question(question_id)
