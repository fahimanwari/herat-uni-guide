from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from .models import RagChunk
from .embeddings import embed_passage
from app.modules.departments.models import Department
from app.modules.news.models import News
from app.modules.faqs.models import Faq
from app.modules.kankor.models import KankorGuide
from app.modules.notifications.models import AcademicEvent


CHUNK_MAX_WORDS = 400


class RagIndexer:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def reindex_all(self) -> int:
        # کتاب‌ها حفظ شوند — فقط chunk‌های غیرکتابی پاک شوند
        await self.db.execute(delete(RagChunk).where(RagChunk.source_type != "book"))
        count = 0
        count += await self._index_departments()
        count += await self._index_news()
        count += await self._index_faqs()
        count += await self._index_guides()
        count += await self._index_events()
        await self.db.commit()
        return count

    async def _index_departments(self) -> int:
        q = (
            select(Department)
            .options(
                selectinload(Department.faculty),
                selectinload(Department.lecture_videos),
            )
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

        intro = f" آشنایی: {d.intro_fa}" if d.intro_fa else ""
        curriculum = ""
        for c in (d.curriculum or []):
            curriculum += f" مضامین سمستر {c['semester']}: {'، '.join(c['subjects'])}."
        videos = ""
        if d.lecture_videos:
            names = "، ".join(f"{v.title_fa} (استاد {v.lecturer_name or 'نامشخص'})" for v in d.lecture_videos if v.is_active)
            videos = f" ویدیوهای درسی موجود: {names}."

        return (
            f"دیپارتمنت {d.name_fa} در پوهنځی {faculty_name} پوهنتون هرات. "
            f"{type_note} "
            f"دیدگاه: {d.vision_fa or ''} ماموریت: {d.mission_fa or ''} "
            f"مدت تحصیل: {d.duration_years} سال، مدرک: {d.degree_type}. "
            f"معرفی: {d.description_fa} "
            f"مضامین اصلی: {'، '.join(d.subjects)}. "
            f"مسیرهای شغلی: {'، '.join(p['title'] for p in d.career_paths)}. "
            f"بازار کار: {d.job_market_fa or ''}"
            f"{intro}{curriculum}{videos}"
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

    async def _index_news(self) -> int:
        q = select(News).where(News.is_published == True)
        items = list((await self.db.execute(q)).scalars())
        count = 0
        for item in items:
            text = f"خبر: {item.title_fa}. {item.body_fa or ''}"
            for chunk in self._split(text):
                self.db.add(RagChunk(source_type="news", source_id=item.id, content=chunk, embedding=embed_passage(chunk)))
                count += 1
        return count

    async def _index_faqs(self) -> int:
        q = select(Faq)
        items = list((await self.db.execute(q)).scalars())
        count = 0
        for item in items:
            text = f"سوال: {item.question_fa}. جواب: {item.answer_fa}"
            for chunk in self._split(text):
                self.db.add(RagChunk(source_type="faq", source_id=item.id, content=chunk, embedding=embed_passage(chunk)))
                count += 1
        return count

    async def _index_guides(self) -> int:
        q = select(KankorGuide)
        items = list((await self.db.execute(q)).scalars())
        count = 0
        for item in items:
            text = f"راهنمای کانکور: {item.title_fa}. {item.body_fa}"
            for chunk in self._split(text):
                self.db.add(RagChunk(source_type="kankor_guide", source_id=item.id, content=chunk, embedding=embed_passage(chunk)))
                count += 1
        return count

    async def _index_events(self) -> int:
        q = select(AcademicEvent).where(AcademicEvent.is_active == True)
        items = list((await self.db.execute(q)).scalars())
        count = 0
        for item in items:
            text = f"رویداد: {item.title_fa} در تاریخ {item.event_date}. {item.description_fa or ''}"
            for chunk in self._split(text):
                self.db.add(RagChunk(source_type="event", source_id=item.id, content=chunk, embedding=embed_passage(chunk)))
                count += 1
        return count
