import uuid
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import get_db
from app.core.security import get_current_admin
from .service import KankorService
from .schemas import ChanceResult, CutoffSchema, CutoffCreate

router = APIRouter(prefix="/kankor", tags=["kankor"])


# --- Public ---

@router.get("/chances", response_model=list[ChanceResult])
async def calculate_chances(
    score: float = Query(..., description="Estimated kankor score"),
    db: AsyncSession = Depends(get_db),
):
    return await KankorService(db).calculate_chances(score)


# --- Admin CRUD ---

@router.get("/cutoffs")
async def list_cutoffs(
    department_id: uuid.UUID | None = None,
    db: AsyncSession = Depends(get_db),
    admin=Depends(get_current_admin),
):
    return await KankorService(db).list_cutoffs(department_id)


@router.post("/cutoffs", response_model=CutoffSchema)
async def create_cutoff(
    payload: CutoffCreate,
    department_id: uuid.UUID = Query(...),
    db: AsyncSession = Depends(get_db),
    admin=Depends(get_current_admin),
):
    return await KankorService(db).create_cutoff(department_id, payload)


@router.delete("/cutoffs/{cutoff_id}")
async def delete_cutoff(
    cutoff_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    admin=Depends(get_current_admin),
):
    return await KankorService(db).delete_cutoff(cutoff_id)
