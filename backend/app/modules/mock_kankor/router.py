import uuid
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import get_db
from app.core.security import get_current_admin
from .service import MockKankorService
from .schemas import (
    StartMockExamRequest, MockExamStartResponse, SubmitMockExamRequest, MockExamResult, MockExamReview,
    ExamBlueprintItem, ExamBlueprintCreate,
)

router = APIRouter(prefix="/mock-kankor", tags=["mock-kankor"])


@router.post("/start", response_model=MockExamStartResponse)
async def start_exam(
    payload: StartMockExamRequest,
    db: AsyncSession = Depends(get_db),
):
    return await MockKankorService(db).start_exam(
        session_id=payload.session_id,
        subject=payload.subject,
        num_questions=payload.num_questions,
        year_filter=payload.year_filter,
        blueprint_id=payload.blueprint_id,
    )


# --- Exam blueprints (structure of a standardized mock exam) ---

@router.get("/blueprints", response_model=list[ExamBlueprintItem])
async def list_blueprints(db: AsyncSession = Depends(get_db)):
    return await MockKankorService(db).list_blueprints()


@router.post("/blueprints", response_model=ExamBlueprintItem, status_code=201)
async def create_blueprint(
    payload: ExamBlueprintCreate,
    db: AsyncSession = Depends(get_db),
    admin=Depends(get_current_admin),
):
    return await MockKankorService(db).create_blueprint(payload)


@router.patch("/blueprints/{blueprint_id}", response_model=ExamBlueprintItem)
async def update_blueprint(
    blueprint_id: uuid.UUID,
    payload: ExamBlueprintItem,
    db: AsyncSession = Depends(get_db),
    admin=Depends(get_current_admin),
):
    return await MockKankorService(db).update_blueprint(blueprint_id, payload)


@router.delete("/blueprints/{blueprint_id}", status_code=204)
async def delete_blueprint(
    blueprint_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    admin=Depends(get_current_admin),
):
    await MockKankorService(db).delete_blueprint(blueprint_id)


@router.post("/{session_id}/submit", response_model=MockExamResult)
async def submit_exam(
    session_id: str,
    payload: SubmitMockExamRequest,
    db: AsyncSession = Depends(get_db),
):
    return await MockKankorService(db).submit_exam(
        session_id=session_id,
        answers=payload.answers,
        time_taken_seconds=payload.time_taken_seconds,
    )


@router.get("/{session_id}/review")
async def review_exam(
    session_id: str,
    db: AsyncSession = Depends(get_db),
):
    return await MockKankorService(db).review_exam(session_id)


@router.get("/history")
async def get_history(
    session_id: str = Query(...),
    db: AsyncSession = Depends(get_db),
):
    return await MockKankorService(db).get_history(session_id)
