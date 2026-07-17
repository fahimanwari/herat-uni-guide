import uuid

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import get_db
from .service import ExamService
from .schemas import (
    ExamListItem, ExamDetail, ExamWithQuestions,
    SubmitExamRequest, ExamResultResponse, UserStats,
)

router = APIRouter(prefix="/exam", tags=["exam"])


@router.get("", response_model=list[ExamListItem])
async def list_exams(
    category: str | None = None,
    db: AsyncSession = Depends(get_db),
):
    return await ExamService(db).list_exams(category)


@router.get("/{exam_id}", response_model=ExamWithQuestions)
async def get_exam(exam_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    return await ExamService(db).get_exam(exam_id)


@router.post("/{exam_id}/submit")
async def submit_exam(
    exam_id: uuid.UUID,
    payload: SubmitExamRequest,
    db: AsyncSession = Depends(get_db),
):
    return await ExamService(db).submit_exam(exam_id, payload)


@router.get("/{exam_id}/stats")
async def get_stats(exam_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    return await ExamService(db).get_stats(exam_id)


@router.get("/{exam_id}/year-comparison")
async def get_year_comparison(exam_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    return await ExamService(db).get_year_comparison(exam_id)


@router.get("/results/{session_id}", response_model=list[ExamResultResponse])
async def get_results(session_id: str, db: AsyncSession = Depends(get_db)):
    return await ExamService(db).get_results(session_id)


@router.get("/stats/{session_id}", response_model=UserStats)
async def get_user_stats(session_id: str, db: AsyncSession = Depends(get_db)):
    return await ExamService(db).get_user_stats(session_id)
