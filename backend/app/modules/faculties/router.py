import uuid

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import get_db
from app.core.security import get_current_admin
from app.modules.admin_auth.models import AdminUser
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
async def create_faculty(
    payload: FacultyCreate,
    db: AsyncSession = Depends(get_db),
    admin: AdminUser = Depends(get_current_admin),
):
    return await FacultyService(db).create_faculty(payload)


@router.patch("/{slug}", response_model=FacultyDetail)
async def update_faculty(
    slug: str,
    payload: FacultyUpdate,
    db: AsyncSession = Depends(get_db),
    admin: AdminUser = Depends(get_current_admin),
):
    return await FacultyService(db).update_faculty(slug, payload)


@router.delete("/{slug}", status_code=204)
async def delete_faculty(
    slug: str,
    db: AsyncSession = Depends(get_db),
    admin: AdminUser = Depends(get_current_admin),
):
    await FacultyService(db).delete_faculty(slug)
