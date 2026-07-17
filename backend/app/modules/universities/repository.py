import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .models import University


class UniversityRepository:
    """Single point of contact with DB for universities (Law 1)"""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def list_all(self) -> list[University]:
        q = select(University).where(University.is_active).order_by(University.name_fa)
        return list((await self.db.execute(q)).scalars())

    async def get_by_slug(self, slug: str) -> University | None:
        q = select(University).where(University.slug == slug)
        return (await self.db.execute(q)).scalar_one_or_none()

    async def get_by_id(self, id: uuid.UUID) -> University | None:
        return await self.db.get(University, id)

    async def create(self, data: dict) -> University:
        obj = University(**data)
        self.db.add(obj)
        await self.db.commit()
        await self.db.refresh(obj)
        return obj

    async def update(self, obj: University, data: dict) -> University:
        for key, value in data.items():
            setattr(obj, key, value)
        await self.db.commit()
        await self.db.refresh(obj)
        return obj

    async def delete(self, obj: University) -> None:
        await self.db.delete(obj)
        await self.db.commit()
