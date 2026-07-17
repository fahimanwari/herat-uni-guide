import uuid

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import get_db
from .service import NewsService
from .schemas import NewsListItem, NewsDetail, NewsCreate, NewsUpdate

router = APIRouter(prefix="/news", tags=["news"])


@router.get("", response_model=list[NewsListItem])
async def list_news(
    university_id: uuid.UUID | None = None, db: AsyncSession = Depends(get_db)
):
    return await NewsService(db).list_news(university_id)


@router.get("/{id}", response_model=NewsDetail)
async def get_news(id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    return await NewsService(db).get_news(id)


@router.post("", response_model=NewsDetail, status_code=201)
async def create_news(payload: NewsCreate, db: AsyncSession = Depends(get_db)):
    return await NewsService(db).create_news(payload)


@router.patch("/{id}", response_model=NewsDetail)
async def update_news(
    id: uuid.UUID, payload: NewsUpdate, db: AsyncSession = Depends(get_db)
):
    return await NewsService(db).update_news(id, payload)
