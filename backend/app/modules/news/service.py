import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import NotFoundError
from .repository import NewsRepository
from .schemas import NewsCreate, NewsUpdate


class NewsService:

    def __init__(self, db: AsyncSession):
        self.repo = NewsRepository(db)

    async def list_news(self, university_id: uuid.UUID | None = None):
        return await self.repo.list_all(university_id, published_only=True)

    async def get_news(self, id: uuid.UUID):
        item = await self.repo.get_by_id(id)
        if item is None:
            raise NotFoundError(f"News '{id}' not found")
        return item

    async def create_news(self, payload: NewsCreate):
        return await self.repo.create(payload.model_dump())

    async def update_news(self, id: uuid.UUID, payload: NewsUpdate):
        item = await self.get_news(id)
        return await self.repo.update(item, payload.model_dump(exclude_unset=True))

    async def delete_news(self, id: uuid.UUID):
        item = await self.get_news(id)
        await self.repo.delete(item)
