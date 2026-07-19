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

        # استخراج کلمات کلیدی
        keywords = [w for w in question.split() if len(w) > 2]

        q = select(RagChunk.content, RagChunk.meta, RagChunk.embedding.cosine_distance(q_emb).label("dist"))
        if source_types:
            q = q.where(RagChunk.source_type.in_(source_types))
        # limit بالاتر برای گرفتن نتایج بیشتر و فیلتر با keyword
        q = q.order_by("dist").limit(limit * 5)
        rows = (await self.db.execute(q)).all()

        # فیلتر با threshold
        if threshold is not None:
            rows = [r for r in rows if r[2] <= threshold]

        # اولویت‌بندی: chunk‌هایی که کلمه کلیدی دارند جلوتر بیایند
        if keywords:
            def score(row):
                content = row[0]
                has_kw = any(kw in content for kw in keywords)
                return (0 if has_kw else 1, row[2])
            rows = sorted(rows, key=score)

        return [(r[0], r[1]) for r in rows[:limit]]
