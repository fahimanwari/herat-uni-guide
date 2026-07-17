from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import get_db
from .indexer import RagIndexer

router = APIRouter(prefix="/admin/rag", tags=["admin"])


@router.post("/reindex")
async def reindex(db: AsyncSession = Depends(get_db)):
    count = await RagIndexer(db).reindex_all()
    return {"chunks_created": count}
