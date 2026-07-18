from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
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
    try:
        count = await RagIndexer(db).reindex_all()
    except ModuleNotFoundError:
        raise HTTPException(
            status_code=503,
            detail="مدل embedding نصب نیست — سرور نیاز به نصب sentence-transformers دارد",
        )
    return {"chunks_created": count}


@router.get("/logs")
async def get_chat_logs(
    page: int = Query(1, ge=1),
    limit: int = Query(20, le=100),
    db: AsyncSession = Depends(get_db),
    admin: AdminUser = Depends(get_current_admin),
):
    from .models import AiChatLog
    offset = (page - 1) * limit
    q = (
        select(AiChatLog)
        .order_by(AiChatLog.created_at.desc())
        .offset(offset)
        .limit(limit)
    )
    logs = list((await db.execute(q)).scalars())
    return [
        {
            "id": str(log.id),
            "session_id": log.session_id,
            "user_message": log.user_message,
            "ai_response": log.ai_response,
            "was_cached": log.was_cached,
            "created_at": log.created_at.isoformat() if log.created_at else None,
        }
        for log in logs
    ]
