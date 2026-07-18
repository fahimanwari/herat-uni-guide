import uuid
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import get_db
from app.core.security import get_current_admin
from .service import QuestionBankService
from .schemas import GenerateExamRequest, QuestionBankItem, QuestionBankCreate

router = APIRouter(prefix="/question-bank", tags=["question-bank"])


# --- Public endpoints ---

@router.get("/stats")
async def get_stats(db: AsyncSession = Depends(get_db)):
    return await QuestionBankService(db).get_stats()


@router.post("/generate-exam")
async def generate_exam(payload: GenerateExamRequest, db: AsyncSession = Depends(get_db)):
    return await QuestionBankService(db).generate_exam(
        subject=payload.subject,
        num_questions=payload.num_questions,
        difficulty=payload.difficulty,
    )


@router.get("/questions")
async def list_questions(
    subject: str | None = None,
    limit: int = Query(50, le=200),
    offset: int = 0,
    db: AsyncSession = Depends(get_db),
):
    return await QuestionBankService(db).list_questions(subject, limit, offset)


# --- Admin CRUD (requires auth) ---

@router.post("/questions", response_model=QuestionBankItem)
async def create_question(
    payload: QuestionBankCreate,
    db: AsyncSession = Depends(get_db),
    admin=Depends(get_current_admin),
):
    return await QuestionBankService(db).create_question(payload)


@router.patch("/questions/{question_id}", response_model=QuestionBankItem)
async def update_question(
    question_id: uuid.UUID,
    payload: QuestionBankItem,
    db: AsyncSession = Depends(get_db),
    admin=Depends(get_current_admin),
):
    return await QuestionBankService(db).update_question(question_id, payload)


@router.delete("/questions/{question_id}")
async def delete_question(
    question_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    admin=Depends(get_current_admin),
):
    return await QuestionBankService(db).delete_question(question_id)


@router.post("/import")
async def import_questions(
    questions: list[QuestionBankItem],
    db: AsyncSession = Depends(get_db),
    admin=Depends(get_current_admin),
):
    return await QuestionBankService(db).import_questions(questions)
