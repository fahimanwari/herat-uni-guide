import uuid
from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .models import News


class NewsRepository:

    def __init__(self, db: AsyncSession):
        self.db = db

    async def list_all(
        self, university_id: uuid.UUID | None = None, published_only: bool = False
    ) -> list[News]:
        q = select(News).order_by(News.created_at.desc())
        if university_id:
            q = q.where(News.university_id == university_id)
        if published_only:
            q = q.where(News.is_published == True)
        return list((await self.db.execute(q)).scalars())

    async def get_by_id(self, id: uuid.UUID) -> News | None:
        return await self.db.get(News, id)

    async def create(self, data: dict) -> News:
        if data.get("is_published") and not data.get("published_at"):
            data["published_at"] = datetime.utcnow()
        obj = News(**data)
        self.db.add(obj)
        await self.db.commit()
        await self.db.refresh(obj)
        return obj

    async def update(self, obj: News, data: dict) -> News:
        for key, value in data.items():
            setattr(obj, key, value)
        await self.db.commit()
        await self.db.refresh(obj)
        return obj

    async def delete(self, obj: News) -> None:
        await self.db.delete(obj)
        await self.db.commit()
