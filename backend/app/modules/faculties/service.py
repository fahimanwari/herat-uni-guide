import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import NotFoundError
from .repository import FacultyRepository
from .schemas import FacultyCreate, FacultyUpdate


class FacultyService:

    def __init__(self, db: AsyncSession):
        self.repo = FacultyRepository(db)

    async def list_faculties(self, university_id: uuid.UUID | None = None):
        return await self.repo.list_all(university_id)

    async def get_faculty(self, slug: str):
        fac = await self.repo.get_by_slug(slug)
        if fac is None:
            raise NotFoundError(f"Faculty '{slug}' not found")
        return fac

    async def create_faculty(self, payload: FacultyCreate):
        return await self.repo.create(payload.model_dump())

    async def update_faculty(self, slug: str, payload: FacultyUpdate):
        fac = await self.get_faculty(slug)
        return await self.repo.update(fac, payload.model_dump(exclude_unset=True))

    async def delete_faculty(self, slug: str):
        fac = await self.get_faculty(slug)
        await self.repo.delete(fac)
