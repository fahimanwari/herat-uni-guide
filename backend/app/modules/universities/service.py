import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import NotFoundError
from .repository import UniversityRepository
from .schemas import UniversityCreate, UniversityUpdate


class UniversityService:
    """Business logic — router only talks to this class"""

    def __init__(self, db: AsyncSession):
        self.repo = UniversityRepository(db)

    async def list_universities(self):
        return await self.repo.list_all()

    async def get_university(self, slug: str):
        uni = await self.repo.get_by_slug(slug)
        if uni is None:
            raise NotFoundError(f"University '{slug}' not found")
        return uni

    async def create_university(self, payload: UniversityCreate):
        return await self.repo.create(payload.model_dump())

    async def update_university(self, slug: str, payload: UniversityUpdate):
        uni = await self.get_university(slug)
        return await self.repo.update(uni, payload.model_dump(exclude_unset=True))

    async def delete_university(self, slug: str):
        uni = await self.get_university(slug)
        await self.repo.delete(uni)
