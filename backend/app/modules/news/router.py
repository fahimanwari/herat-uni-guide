import uuid

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import get_db
from app.core.security import get_current_admin
from app.modules.admin_auth.models import AdminUser
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
async def create_news(
    payload: NewsCreate,
    db: AsyncSession = Depends(get_db),
    admin: AdminUser = Depends(get_current_admin),
):
    return await NewsService(db).create_news(payload)


@router.patch("/{id}", response_model=NewsDetail)
async def update_news(
    id: uuid.UUID,
    payload: NewsUpdate,
    db: AsyncSession = Depends(get_db),
    admin: AdminUser = Depends(get_current_admin),
):
    return await NewsService(db).update_news(id, payload)


@router.delete("/{id}", status_code=204)
async def delete_news(
    id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    admin: AdminUser = Depends(get_current_admin),
):
    await NewsService(db).delete_news(id)
