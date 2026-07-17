from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .models import RagChunk
from .embeddings import embed_query


class RagRetriever:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def retrieve(self, question: str, limit: int = 8) -> list[str]:
        q_emb = embed_query(question)
        rows = await self.db.execute(
            select(RagChunk.content)
            .order_by(RagChunk.embedding.cosine_distance(q_emb))
            .limit(limit)
        )
        return [r[0] for r in rows]
