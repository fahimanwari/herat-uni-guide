import uuid

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import get_db
from .service import FacultyService
from .schemas import FacultyListItem, FacultyDetail, FacultyCreate, FacultyUpdate

router = APIRouter(prefix="/faculties", tags=["faculties"])


@router.get("", response_model=list[FacultyListItem])
async def list_faculties(
    university_id: uuid.UUID | None = None, db: AsyncSession = Depends(get_db)
):
    return await FacultyService(db).list_faculties(university_id)


@router.get("/{slug}", response_model=FacultyDetail)
async def get_faculty(slug: str, db: AsyncSession = Depends(get_db)):
    return await FacultyService(db).get_faculty(slug)


@router.post("", response_model=FacultyDetail, status_code=201)
async def create_faculty(payload: FacultyCreate, db: AsyncSession = Depends(get_db)):
    return await FacultyService(db).create_faculty(payload)


@router.patch("/{slug}", response_model=FacultyDetail)
async def update_faculty(
    slug: str, payload: FacultyUpdate, db: AsyncSession = Depends(get_db)
):
    return await FacultyService(db).update_faculty(slug, payload)
