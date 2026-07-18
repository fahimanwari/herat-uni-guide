from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import get_db
from .service import AchievementService
from .schemas import AchievementSchema

router = APIRouter(prefix="/achievements", tags=["achievements"])


@router.get("", response_model=list[AchievementSchema])
async def get_achievements(
    session_id: str = Query(...),
    db: AsyncSession = Depends(get_db),
):
    return await AchievementService(db).get_achievements(session_id)


@router.get("/leaderboard")
async def get_leaderboard(
    days: int = Query(7, ge=1, le=30),
    db: AsyncSession = Depends(get_db),
):
    return await AchievementService(db).get_leaderboard(days)
