import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .models import Faculty


class FacultyRepository:

    def __init__(self, db: AsyncSession):
        self.db = db

    async def list_all(self, university_id: uuid.UUID | None = None) -> list[Faculty]:
        q = select(Faculty).order_by(Faculty.sort_order, Faculty.name_fa)
        if university_id:
            q = q.where(Faculty.university_id == university_id)
        return list((await self.db.execute(q)).scalars())

    async def get_by_slug(self, slug: str) -> Faculty | None:
        q = select(Faculty).where(Faculty.slug == slug)
        return (await self.db.execute(q)).scalar_one_or_none()

    async def create(self, data: dict) -> Faculty:
        obj = Faculty(**data)
        self.db.add(obj)
        await self.db.commit()
        await self.db.refresh(obj)
        return obj

    async def update(self, obj: Faculty, data: dict) -> Faculty:
        for key, value in data.items():
            setattr(obj, key, value)
        await self.db.commit()
        await self.db.refresh(obj)
        return obj

    async def delete(self, obj: Faculty) -> None:
        await self.db.delete(obj)
        await self.db.commit()
