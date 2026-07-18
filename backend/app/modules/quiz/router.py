import uuid
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import get_db
from app.core.security import get_current_admin
from .service import QuizService
from .schemas import (
    QuestionSchema, QuizMatch, ScoreRequest,
    TraitProfileSchema, TraitProfileCreate, TraitProfileUpdate,
)

router = APIRouter(prefix="/quiz", tags=["quiz"])


# --- Public ---

@router.get("/questions", response_model=list[QuestionSchema])
async def list_questions(db: AsyncSession = Depends(get_db)):
    return await QuizService(db).get_questions()


@router.post("/score", response_model=list[QuizMatch])
async def score_quiz(payload: ScoreRequest, db: AsyncSession = Depends(get_db)):
    return await QuizService(db).score(payload.selected_option_ids)


# --- Admin CRUD: Questions ---

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
    await QuizService(db).delete_question(question_id)


# --- Admin CRUD: Department Trait Profiles ---

@router.get("/profiles", response_model=list[TraitProfileSchema])
async def list_profiles(
    db: AsyncSession = Depends(get_db),
    admin=Depends(get_current_admin),
):
    return await QuizService(db).list_profiles()


@router.post("/profiles", response_model=TraitProfileSchema, status_code=201)
async def create_profile(
    payload: TraitProfileCreate,
    db: AsyncSession = Depends(get_db),
    admin=Depends(get_current_admin),
):
    return await QuizService(db).create_profile(payload)


@router.patch("/profiles/{profile_id}", response_model=TraitProfileSchema)
async def update_profile(
    profile_id: uuid.UUID,
    payload: TraitProfileUpdate,
    db: AsyncSession = Depends(get_db),
    admin=Depends(get_current_admin),
):
    return await QuizService(db).update_profile(profile_id, payload)


@router.delete("/profiles/{profile_id}")
async def delete_profile(
    profile_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    admin=Depends(get_current_admin),
):
    await QuizService(db).delete_profile(profile_id)
