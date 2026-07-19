from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .models import RagChunk
from .embeddings import embed_query


class RagRetriever:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def retrieve(
        self,
        question: str,
        limit: int = 8,
        source_types: list[str] | None = None,
        threshold: float | None = None,
    ) -> list[tuple[str, dict]]:
        q_emb = embed_query(question)
        q = select(RagChunk.content, RagChunk.meta, RagChunk.embedding.cosine_distance(q_emb).label("dist"))
        if source_types:
            q = q.where(RagChunk.source_type.in_(source_types))
        q = q.order_by("dist").limit(limit)
        rows = (await self.db.execute(q)).all()
        if threshold is not None:
            rows = [r for r in rows if r[2] <= threshold]
        return [(r[0], r[1]) for r in rows]
