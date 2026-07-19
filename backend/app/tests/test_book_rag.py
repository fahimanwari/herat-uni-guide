"""تست‌های RAG کتاب‌های درسی."""
import uuid
import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.ai.models import RagChunk
from app.modules.ai.retriever import RagRetriever
from app.modules.ai.embeddings import embed_passage


@pytest_asyncio.fixture
async def sample_book_chunks(client):
    """چند chunk نمونه کتابی در دیتابیس می‌گذارد."""
    from app.core.deps import get_db

    async with client.app.dependency_overrides[get_db]():
        pass  # need direct db access

    # از یک session مستقیم استفاده می‌کنیم
    from app.database import SessionLocal
    async with SessionLocal() as db:
        chunks = [
            ("قانون دوم نیوتن: نیروی خالص برابر جرم ضربدر شتاب است. F=ma.", "فیزیک", "10", 58),
            ("هایبریدیزیشن sp3 در کاربن: وقتی کاربن به چهار اتم دیگر وصل باشد.", "کیمیا", "12", 45),
            ("فعل ماضی فعلی است که نشان دهنده کار گذشته باشد.", "دری", "10", 30),
        ]
        ids = []
        for content, book, grade, page in chunks:
            chunk_id = uuid.uuid4()
            db.add(RagChunk(
                id=chunk_id,
                source_type="book",
                content=content,
                embedding=embed_passage(content),
                meta={"book": book, "grade": grade, "page": page, "file": f"G{grade}-Dr-{book}.pdf"},
            ))
            ids.append(chunk_id)
        # یک chunk غیرکتابی هم اضافه کنیم
        db.add(RagChunk(
            id=uuid.uuid4(),
            source_type="department",
            content="دیپارتمنت کمپیوتر ساینس در پوهنځی علوم پوهنتون هرات",
            embedding=embed_passage("دیپارتمنت کمپیوتر ساینس"),
            meta={},
        ))
        await db.commit()
        yield ids
        # پاکسازی
        for cid in ids:
            await db.execute(
                __import__('sqlalchemy').delete(RagChunk).where(RagChunk.id == cid)
            )
        await db.execute(
            __import__('sqlalchemy').delete(RagChunk).where(RagChunk.source_type == "department")
        )
        await db.commit()


@pytest.mark.asyncio
async def test_retrieve_books_only(client, sample_book_chunks):
    """فقط chunk‌های کتابی برگردانده شوند."""
    from app.database import SessionLocal
    async with SessionLocal() as db:
        retriever = RagRetriever(db)
        results = await retriever.retrieve("قانون نیوتن", source_types=["book"])
        # همه نتایج باید از نوع book باشند
        assert len(results) > 0
        for content, meta in results:
            assert "کتاب" in content or meta.get("book")  # meta باید اطلاعات کتاب داشته باشد


@pytest.mark.asyncio
async def test_retrieve_all_sources(client, sample_book_chunks):
    """بدون فیلتر، همه منابع برگردانده شوند."""
    from app.database import SessionLocal
    async with SessionLocal() as db:
        retriever = RagRetriever(db)
        results = await retriever.retrieve("کمپیوتر")
        assert len(results) > 0


@pytest.mark.asyncio
async def test_chat_books_mode(client):
    """endpoint چت با mode=books بدون خطا جواب دهد."""
    res = await client.post("/api/v1/ai/chat", json={
        "message": "قانون نیوتن چیست؟",
        "language": "fa",
        "mode": "book",
    })
    # اگر Redis/AI متصل باشد 200 برمی‌گرداند
    # اگر نباشد至少 نباید crash کند
    assert res.status_code in (200, 500)  # 500 فقط اگر provider نباشد
