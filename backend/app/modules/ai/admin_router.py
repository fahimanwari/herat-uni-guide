from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import get_db
from app.core.security import get_current_admin
from app.modules.admin_auth.models import AdminUser
from .indexer import RagIndexer

router = APIRouter(prefix="/admin/rag", tags=["admin"])


@router.post("/reindex")
async def reindex(
    db: AsyncSession = Depends(get_db),
    admin: AdminUser = Depends(get_current_admin),
):
    count = await RagIndexer(db).reindex_all()
    return {"chunks_created": count}
