import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from .models import Department, StudentProject, AlumniStory, CareerRoadmap


class DepartmentRepository:

    def __init__(self, db: AsyncSession):
        self.db = db

    async def list_all(
        self,
        faculty_id: uuid.UUID | None = None,
        department_type: str | None = None,
    ) -> list[Department]:
        q = select(Department).order_by(Department.name_fa)
        if faculty_id:
            q = q.where(Department.faculty_id == faculty_id)
        if department_type:
            q = q.where(Department.department_type == department_type)
        return list((await self.db.execute(q)).scalars())

    async def get_by_slug(self, slug: str) -> Department | None:
        q = (
            select(Department)
            .options(
                selectinload(Department.student_projects),
                selectinload(Department.alumni_stories),
                selectinload(Department.career_roadmaps),
            )
            .where(Department.slug == slug)
        )
        return (await self.db.execute(q)).scalar_one_or_none()

    async def create(self, data: dict) -> Department:
        obj = Department(**data)
        self.db.add(obj)
        await self.db.commit()
        await self.db.refresh(obj)
        return obj

    async def update(self, obj: Department, data: dict) -> Department:
        for key, value in data.items():
            setattr(obj, key, value)
        await self.db.commit()
        await self.db.refresh(obj)
        return obj

    async def delete(self, obj: Department) -> None:
        await self.db.delete(obj)
        await self.db.commit()

    # Sub-tables
    async def add_student_project(self, department_id: uuid.UUID, data: dict) -> StudentProject:
        obj = StudentProject(department_id=department_id, **data)
        self.db.add(obj)
        await self.db.commit()
        await self.db.refresh(obj)
        return obj

    async def add_alumni_story(self, department_id: uuid.UUID, data: dict) -> AlumniStory:
        obj = AlumniStory(department_id=department_id, **data)
        self.db.add(obj)
        await self.db.commit()
        await self.db.refresh(obj)
        return obj

    async def add_career_roadmap(self, department_id: uuid.UUID, data: dict) -> CareerRoadmap:
        obj = CareerRoadmap(department_id=department_id, **data)
        self.db.add(obj)
        await self.db.commit()
        await self.db.refresh(obj)
        return obj
