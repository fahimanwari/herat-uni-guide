import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .models import Faq


class FaqRepository:

    def __init__(self, db: AsyncSession):
        self.db = db

    async def list_all(self, university_id: uuid.UUID | None = None) -> list[Faq]:
        q = select(Faq).order_by(Faq.sort_order, Faq.created_at.desc())
        if university_id:
            q = q.where(Faq.university_id == university_id)
        return list((await self.db.execute(q)).scalars())

    async def get_by_id(self, id: uuid.UUID) -> Faq | None:
        return await self.db.get(Faq, id)

    async def create(self, data: dict) -> Faq:
        obj = Faq(**data)
        self.db.add(obj)
        await self.db.commit()
        await self.db.refresh(obj)
        return obj

    async def update(self, obj: Faq, data: dict) -> Faq:
        for key, value in data.items():
            setattr(obj, key, value)
        await self.db.commit()
        await self.db.refresh(obj)
        return obj

    async def delete(self, obj: Faq) -> None:
        await self.db.delete(obj)
        await self.db.commit()
