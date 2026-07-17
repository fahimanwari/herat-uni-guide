from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import get_db
from .service import QuestionBankService
from .schemas import GenerateExamRequest

router = APIRouter(prefix="/question-bank", tags=["question-bank"])


@router.get("/stats")
async def get_stats(db: AsyncSession = Depends(get_db)):
    """Get statistics about the question bank."""
    return await QuestionBankService(db).get_stats()


@router.get("/subjects")
async def get_subjects(db: AsyncSession = Depends(get_db)):
    """Get all available subjects."""
    return await QuestionBankService(db).get_stats()


@router.post("/generate-exam")
async def generate_exam(payload: GenerateExamRequest, db: AsyncSession = Depends(get_db)):
    """Generate a random exam from the question bank."""
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
    """List questions from the bank."""
    return await QuestionBankService(db).list_questions(subject, limit, offset)
