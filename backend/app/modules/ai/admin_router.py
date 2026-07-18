from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import get_db
from app.core.security import get_current_admin
from app.modules.admin_auth.models import AdminUser
from app.config import settings
from .indexer import RagIndexer

router = APIRouter(prefix="/admin/ai", tags=["admin-ai"])


@router.get("/status")
async def ai_status(admin: AdminUser = Depends(get_current_admin)):
    return {
        "provider": settings.ai_provider,
        "model": settings.ai_model,
        "has_api_key": bool(settings.ai_api_key),
    }


@router.post("/reindex")
async def reindex(
    db: AsyncSession = Depends(get_db),
    admin: AdminUser = Depends(get_current_admin),
):
    from ..ai.indexer import RagIndexer
    count = await RagIndexer(db).reindex_all()
    return {"chunks_created": count}
