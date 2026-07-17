import uuid

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import get_db
from app.core.security import get_current_admin
from app.modules.admin_auth.models import AdminUser
from .service import FaqService
from .schemas import FaqListItem, FaqDetail, FaqCreate, FaqUpdate

router = APIRouter(prefix="/faqs", tags=["faqs"])


@router.get("", response_model=list[FaqListItem])
async def list_faqs(
    university_id: uuid.UUID | None = None, db: AsyncSession = Depends(get_db)
):
    return await FaqService(db).list_faqs(university_id)


@router.get("/{id}", response_model=FaqDetail)
async def get_faq(id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    return await FaqService(db).get_faq(id)


@router.post("", response_model=FaqDetail, status_code=201)
async def create_faq(
    payload: FaqCreate,
    db: AsyncSession = Depends(get_db),
    admin: AdminUser = Depends(get_current_admin),
):
    return await FaqService(db).create_faq(payload)


@router.patch("/{id}", response_model=FaqDetail)
async def update_faq(
    id: uuid.UUID,
    payload: FaqUpdate,
    db: AsyncSession = Depends(get_db),
    admin: AdminUser = Depends(get_current_admin),
):
    return await FaqService(db).update_faq(id, payload)


@router.delete("/{id}", status_code=204)
async def delete_faq(
    id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    admin: AdminUser = Depends(get_current_admin),
):
    await FaqService(db).delete_faq(id)
