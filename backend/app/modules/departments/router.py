import uuid

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import get_db
from .service import DepartmentService
from .schemas import (
    DepartmentListItem, DepartmentDetail, DepartmentCreate, DepartmentUpdate,
    StudentProjectSchema, StudentProjectCreate,
    AlumniStorySchema, AlumniStoryCreate,
    CareerRoadmapSchema, CareerRoadmapCreate,
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
    payload: DepartmentCreate, db: AsyncSession = Depends(get_db)
):
    return await DepartmentService(db).create_department(payload)


@router.patch("/{slug}", response_model=DepartmentDetail)
async def update_department(
    slug: str, payload: DepartmentUpdate, db: AsyncSession = Depends(get_db)
):
    return await DepartmentService(db).update_department(slug, payload)


# --- Sub-tables ---

@router.post("/{slug}/projects", response_model=StudentProjectSchema, status_code=201)
async def add_student_project(
    slug: str, payload: StudentProjectCreate, db: AsyncSession = Depends(get_db)
):
    return await DepartmentService(db).add_student_project(slug, payload)


@router.post("/{slug}/alumni", response_model=AlumniStorySchema, status_code=201)
async def add_alumni_story(
    slug: str, payload: AlumniStoryCreate, db: AsyncSession = Depends(get_db)
):
    return await DepartmentService(db).add_alumni_story(slug, payload)


@router.post("/{slug}/roadmaps", response_model=CareerRoadmapSchema, status_code=201)
async def add_career_roadmap(
    slug: str, payload: CareerRoadmapCreate, db: AsyncSession = Depends(get_db)
):
    return await DepartmentService(db).add_career_roadmap(slug, payload)
