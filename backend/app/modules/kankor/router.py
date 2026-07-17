from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import get_db
from .service import KankorService
from .schemas import ChanceResult

router = APIRouter(prefix="/kankor", tags=["kankor"])


@router.get("/chances", response_model=list[ChanceResult])
async def calculate_chances(
    score: float = Query(..., description="Estimated kankor score"),
    db: AsyncSession = Depends(get_db),
):
    return await KankorService(db).calculate_chances(score)
