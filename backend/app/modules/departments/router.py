import uuid

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import get_db
from app.core.security import get_current_admin
from app.modules.admin_auth.models import AdminUser
from .service import DepartmentService
from .schemas import (
    DepartmentListItem, DepartmentDetail, DepartmentCreate, DepartmentUpdate,
    StudentProjectSchema, StudentProjectCreate,
    AlumniStorySchema, AlumniStoryCreate,
    CareerRoadmapSchema, CareerRoadmapCreate,
    DepartmentVideoSchema, DepartmentVideoCreate,
)

router = APIRouter(prefix="/departments", tags=["departments"])


@router.get("", response_model=list[DepartmentListItem])
async def list_departments(
    faculty_id: uuid.UUID | None = None, db: AsyncSession = Depends(get_db)
):
    return await DepartmentService(db).list_departments(faculty_id)


@router.get("/{slug}", response_model=DepartmentDetail)
async def get_department(slug: str, db: AsyncSession = Depends(get_db)):
    return await DepartmentService(db).get_department(slug)


@router.post("", response_model=DepartmentDetail, status_code=201)
async def create_department(
    payload: DepartmentCreate,
    db: AsyncSession = Depends(get_db),
    admin: AdminUser = Depends(get_current_admin),
):
    return await DepartmentService(db).create_department(payload)


@router.patch("/{slug}", response_model=DepartmentDetail)
async def update_department(
    slug: str,
    payload: DepartmentUpdate,
    db: AsyncSession = Depends(get_db),
    admin: AdminUser = Depends(get_current_admin),
):
    return await DepartmentService(db).update_department(slug, payload)


@router.delete("/{slug}", status_code=204)
async def delete_department(
    slug: str,
    db: AsyncSession = Depends(get_db),
    admin: AdminUser = Depends(get_current_admin),
):
    await DepartmentService(db).delete_department(slug)


# --- Sub-tables ---

@router.post("/{slug}/projects", response_model=StudentProjectSchema, status_code=201)
async def add_student_project(
    slug: str,
    payload: StudentProjectCreate,
    db: AsyncSession = Depends(get_db),
    admin: AdminUser = Depends(get_current_admin),
):
    return await DepartmentService(db).add_student_project(slug, payload)


@router.post("/{slug}/alumni", response_model=AlumniStorySchema, status_code=201)
async def add_alumni_story(
    slug: str,
    payload: AlumniStoryCreate,
    db: AsyncSession = Depends(get_db),
    admin: AdminUser = Depends(get_current_admin),
):
    return await DepartmentService(db).add_alumni_story(slug, payload)


@router.post("/{slug}/roadmaps", response_model=CareerRoadmapSchema, status_code=201)
async def add_career_roadmap(
    slug: str,
    payload: CareerRoadmapCreate,
    db: AsyncSession = Depends(get_db),
    admin: AdminUser = Depends(get_current_admin),
):
    return await DepartmentService(db).add_career_roadmap(slug, payload)


@router.post("/{slug}/videos", response_model=DepartmentVideoSchema, status_code=201)
async def add_video(
    slug: str,
    payload: DepartmentVideoCreate,
    db: AsyncSession = Depends(get_db),
    admin: AdminUser = Depends(get_current_admin),
):
    return await DepartmentService(db).add_video(slug, payload)


@router.delete("/{slug}/videos/{video_id}")
async def delete_video(
    slug: str,
    video_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    admin: AdminUser = Depends(get_current_admin),
):
    await DepartmentService(db).delete_video(slug, video_id)
