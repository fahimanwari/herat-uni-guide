"""ایندکس کتاب‌های درسی وزارت معارف در RAG.
اجرا:  cd backend && .venv/bin/python jobs/index_books.py            # همه کتاب‌ها
       .venv/bin/python jobs/index_books.py G10-Dr-physic.pdf       # فقط یک کتاب
قابل قطع/ادامه است: کتابی که قبلاً ایندکس شده رد می‌شود."""
import asyncio, subprocess, sys, unicodedata, uuid
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from sqlalchemy import select, func
from app.database import SessionLocal
from app.modules.ai.models import RagChunk
from app.modules.ai.embeddings import embed_passage

# import all models so SQLAlchemy knows all tables (needed for FK resolution)
from app.modules.universities.models import University  # noqa: F401
from app.modules.faculties.models import Faculty  # noqa: F401
from app.modules.kankor.models import KankorCutoff, KankorGuide  # noqa: F401
from app.modules.departments.models import Department  # noqa: F401
from app.modules.quiz.models import QuizQuestion, QuizOption, DepartmentTraitProfile  # noqa: F401
from app.modules.admin_auth.models import AdminUser, RefreshToken  # noqa: F401
from app.modules.notifications.models import AcademicEvent  # noqa: F401
from app.modules.news.models import News  # noqa: F401
from app.modules.faqs.models import Faq  # noqa: F401

BOOKS_DIR = Path(__file__).parent.parent.parent / "books"

# نام فایل → (نام دری کتاب، صنف)
BOOK_INFO = {
    # صنف ۱۰ (۱۵ کتاب)
    "G10-Dr-Math.pdf": ("ریاضی", "10"),
    "G10-Dr-physic.pdf": ("فزیک", "10"),
    "G10-Dr-Chemistry.pdf": ("کیمیا", "10"),
    "G10-Dr-Biology.pdf": ("بیولوژی", "10"),
    "G10-Dr-Dari.pdf": ("دری", "10"),
    "G10-Dr-Pashto.pdf": ("پشتو", "10"),
    "G10-Ps-English.pdf": ("انگلیسی", "10"),
    "G10-Dr-History.pdf": ("تاریخ", "10"),
    "G10-Dr-Geography.pdf": ("جغرافیه", "10"),
    "G10-Dr-Geology.pdf": ("جیولوژی", "10"),
    "G10-Dr-Civic.pdf": ("تعلیمات مدنی", "10"),
    "G10-Dr-Computer.pdf": ("کمپیوتر", "10"),
    "G10-Dr-Islamic_Study_hanafi.pdf": ("تعلیمات اسلامی (حنفی)", "10"),
    "G10-Dr-Islamic_Study_jafari.pdf": ("تعلیمات اسلامی (جعفری)", "10"),
    "G10-Dr-Tafseer.pdf": ("تفسیر شریف", "10"),
    # صنف ۱۱ (۱۴ کتاب)
    "G11-Dr-Math.pdf": ("ریاضی", "11"),
    "G11-Dr-Physic.pdf": ("فزیک", "11"),
    "G11-Dr-Chemistry.pdf": ("کیمیا", "11"),
    "G11-Dr-Biology.pdf": ("بیولوژی", "11"),
    "G11-Dr-Dari.pdf": ("دری", "11"),
    "G11-Dr-Pashto.pdf": ("پشتو", "11"),
    "G11-Ps-English.pdf": ("انگلیسی", "11"),
    "G11-Dr-History.pdf": ("تاریخ", "11"),
    "G11-Dr-Geography.pdf": ("جغرافیه", "11"),
    "G11-Dr-CIvic.pdf": ("تعلیمات مدنی", "11"),
    "G11-Dr-Computer.pdf": ("کمپیوتر", "11"),
    "G11-Dr-Islamic_Study_Hanafi.pdf": ("تعلیمات اسلامی (حنفی)", "11"),
    "G11-Dr-Islamic_Study_Jafari.pdf": ("تعلیمات اسلامی (جعفری)", "11"),
    "G11-Dr-Tafseer.pdf": ("تفسیر شریف", "11"),
    # صنف ۱۲ (۱۴ کتاب)
    "G12-Dr-Math.pdf": ("ریاضی", "12"),
    "G12-Dr-Physic.pdf": ("فزیک", "12"),
    "G12-Dr-Chemistry.pdf": ("کیمیا", "12"),
    "G12-Dr-Biology.pdf": ("بیولوژی", "12"),
    "G12-Dr-Dari.pdf": ("دری", "12"),
    "G12-Dr-Pashto.pdf": ("پشتو", "12"),
    "G12-Ps-English.pdf": ("انگلیسی", "12"),
    "G12-Dr-History.pdf": ("تاریخ", "12"),
    "G12-Dr-Geography.pdf": ("جغرافیه", "12"),
    "G12-Dr-Civic.pdf": ("تعلیمات مدنی", "12"),
    "G12-Dr-Computer.pdf": ("کمپیوتر", "12"),
    "G12-Dr-Islamic_Study_Hanafi.pdf": ("تعلیمات اسلامی (حنفی)", "12"),
    "G12-Dr-Islamic_Study_Jafari.pdf": ("تعلیمات اسلامی (جعفری)", "12"),
    "G12-Dr-Tafseer.pdf": ("تفسیر شریف", "12"),
}

MIN_CHARS = 100  # صفحات خیلی کوتاه (جلد، سفید) رد شوند


def extract_page(pdf: Path, page: int) -> str:
    out = subprocess.run(
        ["pdftotext", "-f", str(page), "-l", str(page), str(pdf), "-"],
        capture_output=True, text=True, timeout=30,
    ).stdout
    # حروف نمایشی عربی (ﻣﻰتﻮاﻧﻴد) → حروف استاندارد (می‌توانید)
    return unicodedata.normalize("NFKC", out).strip()


def page_count(pdf: Path) -> int:
    info = subprocess.run(["pdfinfo", str(pdf)], capture_output=True, text=True).stdout
    return int(next(l for l in info.splitlines() if l.startswith("Pages")).split()[-1])


async def index_book(db, filename: str):
    book_name, grade = BOOK_INFO[filename]
    pdf = BOOKS_DIR / filename

    if not pdf.exists():
        print(f"❌ {filename} یافت نشد — رد شد")
        return 0

    already = (await db.execute(
        select(func.count(RagChunk.id)).where(
            RagChunk.source_type == "book",
            RagChunk.meta["file"].as_string() == filename,
        )
    )).scalar()
    if already and already > 10:
        print(f"⏭  {filename} قبلاً ایندکس شده ({already} chunk) — رد شد")
        return 0

    n = 0
    for page in range(1, page_count(pdf) + 1):
        text = extract_page(pdf, page)
        if len(text) < MIN_CHARS:
            continue
        content = f"کتاب {book_name} صنف {grade}، صفحه {page}:\n{text}"
        db.add(RagChunk(
            id=uuid.uuid4(),
            source_type="book",
            content=content,
            embedding=embed_passage(content[:2000]),
            meta={"book": book_name, "grade": grade, "page": page, "file": filename},
        ))
        n += 1
        if n % 50 == 0:
            await db.commit()
            print(f"   ... {filename}: {n} صفحه")
    await db.commit()
    print(f"✅ {filename}: {n} chunk")
    return n


async def main():
    targets = sys.argv[1:] if len(sys.argv) > 1 else list(BOOK_INFO.keys())
    async with SessionLocal() as db:
        total = 0
        for f in targets:
            if f not in BOOK_INFO:
                print(f"⚠️  {f} در لیست نیست — رد شد")
                continue
            total += await index_book(db, f)
        print(f"\nتمام: {total} chunk جدید")

asyncio.run(main())
