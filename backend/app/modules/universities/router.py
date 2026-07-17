from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import get_db
from .service import UniversityService
from .schemas import UniversityListItem, UniversityDetail, UniversityCreate, UniversityUpdate

router = APIRouter(prefix="/universities", tags=["universities"])


@router.get("", response_model=list[UniversityListItem])
async def list_universities(db: AsyncSession = Depends(get_db)):
    return await UniversityService(db).list_universities()


@router.get("/{slug}", response_model=UniversityDetail)
async def get_university(slug: str, db: AsyncSession = Depends(get_db)):
    return await UniversityService(db).get_university(slug)


@router.post("", response_model=UniversityDetail, status_code=201)
async def create_university(
    payload: UniversityCreate, db: AsyncSession = Depends(get_db)
):
    return await UniversityService(db).create_university(payload)


@router.patch("/{slug}", response_model=UniversityDetail)
async def update_university(
    slug: str, payload: UniversityUpdate, db: AsyncSession = Depends(get_db)
):
    return await UniversityService(db).update_university(slug, payload)
