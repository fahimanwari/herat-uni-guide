from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from .models import RagChunk
from .embeddings import embed_passage
from app.modules.departments.models import Department


CHUNK_MAX_WORDS = 400


class RagIndexer:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def reindex_all(self) -> int:
        await self.db.execute(delete(RagChunk))
        count = 0
        count += await self._index_departments()
        await self.db.commit()
        return count

    async def _index_departments(self) -> int:
        q = (
            select(Department)
            .options(selectinload(Department.faculty))
        )
        depts = list((await self.db.execute(q)).scalars())
        count = 0
        for d in depts:
            text = self._department_to_text(d)
            for chunk in self._split(text):
                self.db.add(RagChunk(
                    source_type="department",
                    source_id=d.id,
                    content=chunk,
                    embedding=embed_passage(chunk),
                ))
                count += 1
        return count

    def _department_to_text(self, d) -> str:
        if d.department_type == "service":
            type_note = ("این یک دیپارتمنت خدماتی (غیرفارغ‌ده) است: فقط خدمات آموزشی "
                         "به دیپارتمنت‌های دیگر می‌دهد و در کانکور قابل انتخاب نیست.")
        else:
            type_note = "این یک دیپارتمنت فارغ‌ده است و در کانکور قابل انتخاب است."

        faculty_name = d.faculty.name_fa if d.faculty else "نامعلوم"

        return (
            f"دیپارتمنت {d.name_fa} در پوهنځی {faculty_name} پوهنتون هرات. "
            f"{type_note} "
            f"دیدگاه: {d.vision_fa or ''} ماموریت: {d.mission_fa or ''} "
            f"مدت تحصیل: {d.duration_years} سال، مدرک: {d.degree_type}. "
            f"معرفی: {d.description_fa} "
            f"مضامین اصلی: {'، '.join(d.subjects)}. "
            f"مسیرهای شغلی: {'، '.join(p['title'] for p in d.career_paths)}. "
            f"بازار کار: {d.job_market_fa or ''}"
        )

    def _split(self, text: str) -> list[str]:
        words = text.split()
        chunks, current = [], []
        for w in words:
            current.append(w)
            if len(current) >= CHUNK_MAX_WORDS and w.endswith(("۔", ".", "؟", "!")):
                chunks.append(" ".join(current))
                current = []
        if current:
            chunks.append(" ".join(current))
        return chunks
