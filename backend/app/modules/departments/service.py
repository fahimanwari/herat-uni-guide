import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import NotFoundError
from .repository import DepartmentRepository
from .schemas import (
    DepartmentCreate, DepartmentUpdate,
    StudentProjectCreate, AlumniStoryCreate, CareerRoadmapCreate,
)


class DepartmentService:

    def __init__(self, db: AsyncSession):
        self.repo = DepartmentRepository(db)

    async def list_departments(self, faculty_id: uuid.UUID | None = None):
        return await self.repo.list_all(faculty_id)

    async def get_department(self, slug: str):
        dept = await self.repo.get_by_slug(slug)
        if dept is None:
            raise NotFoundError(f"Department '{slug}' not found")
        return dept

    async def create_department(self, payload: DepartmentCreate):
        return await self.repo.create(payload.model_dump())

    async def update_department(self, slug: str, payload: DepartmentUpdate):
        dept = await self.get_department(slug)
        return await self.repo.update(dept, payload.model_dump(exclude_unset=True))

    async def delete_department(self, slug: str):
        dept = await self.get_department(slug)
        await self.repo.delete(dept)

    # Sub-tables
    async def add_student_project(self, slug: str, payload: StudentProjectCreate):
        dept = await self.get_department(slug)
        return await self.repo.add_student_project(dept.id, payload.model_dump())

    async def add_alumni_story(self, slug: str, payload: AlumniStoryCreate):
        dept = await self.get_department(slug)
        return await self.repo.add_alumni_story(dept.id, payload.model_dump())

    async def add_career_roadmap(self, slug: str, payload: CareerRoadmapCreate):
        dept = await self.get_department(slug)
        return await self.repo.add_career_roadmap(dept.id, payload.model_dump())

    async def add_video(self, slug: str, payload):
        dept = await self.get_department(slug)
        return await self.repo.add_video(dept.id, payload.model_dump())

    async def delete_video(self, slug: str, video_id: uuid.UUID):
        from sqlalchemy import select
        from .models import DepartmentVideo

        dept = await self.get_department(slug)
        q = select(DepartmentVideo).where(
            DepartmentVideo.id == video_id,
            DepartmentVideo.department_id == dept.id,
        )
        obj = (await self.repo.db.execute(q)).scalar_one_or_none()
        if obj is None:
            raise NotFoundError("ویدیو یافت نشد")
        await self.repo.db.delete(obj)
        await self.repo.db.commit()
