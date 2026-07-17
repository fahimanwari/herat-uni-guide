import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import NotFoundError
from .repository import FaqRepository
from .schemas import FaqCreate, FaqUpdate


class FaqService:

    def __init__(self, db: AsyncSession):
        self.repo = FaqRepository(db)

    async def list_faqs(self, university_id: uuid.UUID | None = None):
        return await self.repo.list_all(university_id)

    async def get_faq(self, id: uuid.UUID):
        faq = await self.repo.get_by_id(id)
        if faq is None:
            raise NotFoundError(f"FAQ '{id}' not found")
        return faq

    async def create_faq(self, payload: FaqCreate):
        return await self.repo.create(payload.model_dump())

    async def update_faq(self, id: uuid.UUID, payload: FaqUpdate):
        faq = await self.get_faq(id)
        return await self.repo.update(faq, payload.model_dump(exclude_unset=True))

    async def delete_faq(self, id: uuid.UUID):
        faq = await self.get_faq(id)
        await self.repo.delete(faq)
