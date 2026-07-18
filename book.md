# 📚 book.md — دستیار کتاب‌های درسی: ۴۳ کتاب رسمی وزارت معارف + جواب با ذکر منبع

**تاریخ:** ۱۸ جولای ۲۰۲۶ · **مبنا:** فایل b.md (ایده: Groq از روی ۳۶ کتاب جواب بدهد) + تحقیق و دانلود واقعی
**مخاطب:** تیم توسعه — به سبک new-plan.md: هر گام = کدام فایل، چه کد، چطور تست.

---

# بخش ۰: چه چیزی همین حالا انجام شده ✅ (شما انجام ندهید — فقط بدانید)

| کار | نتیجه |
|---|---|
| پیدا کردن منبع رسمی کتاب‌ها | صفحه «کتب نصاب تعلیمی» وزارت معارف: [moe.gov.af/dr/كتب-نصاب-تعليمى](https://moe.gov.af/dr/%D9%83%D8%AA%D8%A8-%D9%86%D8%B5%D8%A7%D8%A8-%D8%AA%D8%B9%D9%84%D9%8A%D9%85%D9%89) — لینک مستقیم PDF، نصاب فعلی (آپلود رسمی ۲۰۲۰ = چاپ‌های ۱۳۹۸+، قدیمی نیست) |
| **دانلود هر ۴۳ کتاب صنوف ۱۰/۱۱/۱۲** | ✅ کامل — پوشه `books/` پروژه، ۶۳۸ MB، هر ۴۳ فایل سالم (سرخط `%PDF` چک شد) |
| `books/` به `.gitignore` اضافه شد | PDF ها **هرگز** داخل git نمی‌روند (۶۳۸ MB!) — روی سرور جدا کاپی شوند (`scp` یا rsync) |
| تست استخراج متن | ✅ کتاب‌ها **متن واقعی دارند، اسکن تصویری نیستند** — `pdftotext` (نصب است: `/usr/bin/pdftotext`) متن دری سالم می‌دهد → **OCR لازم نیست** 🎉 |
| ⚠️ یک یافته فنی مهم | متن استخراجی با «حروف نمایشی عربی» است (مثلاً `ﻣﻰتﻮاﻧﻴد`) — قبل از ذخیره باید با `unicodedata.normalize("NFKC", text)` نرمال شود وگرنه جستجوی برداری خراب می‌شود. در اسکریپت گام ۳ گذاشته شده. |

**چرا ۴۳ و نه ۳۶؟** لیست رسمی هر صنف ≈۱۴-۱۵ کتاب است چون «تعلیمات اسلامی» دو نسخه دارد (حنفی + جعفری) و «تفسیر شریف» جداست. همه را دانلود کردیم — ۳۶ کتاب اصلی + نسخه‌های اضافی. ضرری ندارد، پوشش کامل‌تر است.

---

# بخش ۱: معماری — یک اصلاح مهم نسبت به b.md

پیشنهاد b.md (چانک → Vector DB → بازیابی → Groq) **دقیقاً درست است** و اتفاقاً **همین حالا در کدبیس ما ساخته شده**:

| جزء پیشنهادی b.md | معادل موجود در کدبیس ما |
|---|---|
| ذخیره PDF ها روی سرور | ✅ پوشه `books/` |
| استخراج متن + چانک | باید ساخته شود (گام ۳ پایین) |
| Vector DB (ChromaDB یا FAISS) | ✅ **از قبل داریم: PostgreSQL + pgvector** — جدول `rag_chunks` + امبدینگ `multilingual-e5-small` + جستجوی cosine در `ai/retriever.py` |
| فرستادن فقط بخش‌های مرتبط به Groq | ✅ `ai/service.py` همین کار را می‌کند (top-8 chunk) |

**تصمیم معماری: ChromaDB/FAISS نصب نکنید.** یک دیتابیس برداری دوم = یک سیستم اضافه برای نگهداری، backup و sync — بدون هیچ مزیتی. pgvector ما همین کار را می‌کند و دیتایش با بقیه سیستم یکجا backup می‌شود. فقط ۳ چیز کم داریم:
1. ستون `meta` روی `rag_chunks` (برای کتاب/صنف/صفحه → **ذکر منبع در جواب**)
2. اسکریپت ایندکس کتاب‌ها
3. حالت «فقط از کتاب‌ها» در چت

---

# بخش ۲: چک‌لیست ۴۳ کتاب

وضعیت: **دانلود = همه ✅**. ستون‌های بعدی را حین کار تیک بزنید.
نام فایل‌ها در `books/` دقیقاً همین است (الگو: `G<صنف>-Dr-<مضمون>.pdf`؛ انگلیسی با پیشوند `Ps`).

## صنف ۱۰ (۱۵ کتاب)
| کتاب | فایل | استخراج | ایندکس | تست سوال |
|---|---|---|---|---|
| ریاضی | G10-Dr-Math.pdf | ☐ | ☐ | ☐ |
| فزیک | G10-Dr-physic.pdf ⚠️(p کوچک) | ☐ | ☐ | ☐ |
| کیمیا | G10-Dr-Chemistry.pdf | ☐ | ☐ | ☐ |
| بیولوژی | G10-Dr-Biology.pdf | ☐ | ☐ | ☐ |
| دری | G10-Dr-Dari.pdf | ☐ | ☐ | ☐ |
| پشتو | G10-Dr-Pashto.pdf | ☐ | ☐ | ☐ |
| انگلیسی | G10-Ps-English.pdf | ☐ | ☐ | ☐ |
| تاریخ | G10-Dr-History.pdf | ☐ | ☐ | ☐ |
| جغرافیه | G10-Dr-Geography.pdf | ☐ | ☐ | ☐ |
| جیولوژی | G10-Dr-Geology.pdf | ☐ | ☐ | ☐ |
| تعلیمات مدنی | G10-Dr-Civic.pdf | ☐ | ☐ | ☐ |
| کمپیوتر | G10-Dr-Computer.pdf | ☐ | ☐ | ☐ |
| تعلیمات اسلامی (حنفی) | G10-Dr-Islamic_Study_hanafi.pdf | ☐ | ☐ | ☐ |
| تعلیمات اسلامی (جعفری) | G10-Dr-Islamic_Study_jafari.pdf | ☐ | ☐ | ☐ |
| تفسیر شریف | G10-Dr-Tafseer.pdf | ☐ | ☐ | ☐ |

## صنف ۱۱ (۱۴ کتاب)
| کتاب | فایل | استخراج | ایندکس | تست سوال |
|---|---|---|---|---|
| ریاضی | G11-Dr-Math.pdf | ☐ | ☐ | ☐ |
| فزیک | G11-Dr-Physic.pdf | ☐ | ☐ | ☐ |
| کیمیا | G11-Dr-Chemistry.pdf | ☐ | ☐ | ☐ |
| بیولوژی | G11-Dr-Biology.pdf | ☐ | ☐ | ☐ |
| دری | G11-Dr-Dari.pdf | ☐ | ☐ | ☐ |
| پشتو | G11-Dr-Pashto.pdf | ☐ | ☐ | ☐ |
| انگلیسی | G11-Ps-English.pdf | ☐ | ☐ | ☐ |
| تاریخ | G11-Dr-History.pdf | ☐ | ☐ | ☐ |
| جغرافیه | G11-Dr-Geography.pdf | ☐ | ☐ | ☐ |
| تعلیمات مدنی | G11-Dr-CIvic.pdf ⚠️(I بزرگ) | ☐ | ☐ | ☐ |
| کمپیوتر | G11-Dr-Computer.pdf | ☐ | ☐ | ☐ |
| تعلیمات اسلامی (حنفی) | G11-Dr-Islamic_Study_Hanafi.pdf | ☐ | ☐ | ☐ |
| تعلیمات اسلامی (جعفری) | G11-Dr-Islamic_Study_Jafari.pdf | ☐ | ☐ | ☐ |
| تفسیر شریف | G11-Dr-Tafseer.pdf | ☐ | ☐ | ☐ |

## صنف ۱۲ (۱۴ کتاب)
| کتاب | فایل | استخراج | ایندکس | تست سوال |
|---|---|---|---|---|
| ریاضی | G12-Dr-Math.pdf | ☐ | ☐ | ☐ |
| فزیک | G12-Dr-Physic.pdf | ☐ | ☐ | ☐ |
| کیمیا | G12-Dr-Chemistry.pdf | ☐ | ☐ | ☐ |
| بیولوژی | G12-Dr-Biology.pdf | ☐ | ☐ | ☐ |
| دری | G12-Dr-Dari.pdf | ☐ | ☐ | ☐ |
| پشتو | G12-Dr-Pashto.pdf | ☐ | ☐ | ☐ |
| انگلیسی | G12-Ps-English.pdf | ☐ | ☐ | ☐ |
| تاریخ | G12-Dr-History.pdf | ☐ | ☐ | ☐ |
| جغرافیه | G12-Dr-Geography.pdf | ☐ | ☐ | ☐ |
| تعلیمات مدنی | G12-Dr-Civic.pdf | ☐ | ☐ | ☐ |
| کمپیوتر | G12-Dr-Computer.pdf | ☐ | ☐ | ☐ |
| تعلیمات اسلامی (حنفی) | G12-Dr-Islamic_Study_Hanafi.pdf | ☐ | ☐ | ☐ |
| تعلیمات اسلامی (جعفری) | G12-Dr-Islamic_Study_Jafari.pdf | ☐ | ☐ | ☐ |
| تفسیر شریف | G12-Dr-Tafseer.pdf | ☐ | ☐ | ☐ |

اگر کتابی دوباره لازم شد: `https://moe.gov.af/sites/default/files/2020-03/<نام-فایل>` (لیست کامل لینک‌ها هم در همان صفحه وزارت).

---

# بخش ۳: گام‌های کد (به ترتیب — مجموعاً ~۳-۴ روز)

## گام ۱ — ستون meta روی rag_chunks (نیم ساعت)

**فایل `backend/app/modules/ai/models.py`** — به class `RagChunk` اضافه کنید:
```python
    meta: Mapped[dict] = mapped_column(JSON, default=dict)
    # برای کتاب‌ها: {"book": "فزیک", "grade": "10", "page": 58, "file": "G10-Dr-physic.pdf"}
```
(بالای فایل `JSON` را به import های sqlalchemy اضافه کنید.) بعد:
```bash
cd backend
.venv/bin/alembic revision --autogenerate -m "rag_chunks meta column"
# فایل ساخته‌شده را بخوانید — فقط add_column باشد
.venv/bin/alembic upgrade head
```

## گام ۲ — ⚠️ اول این باگ آینده را ببندید (۱۰ دقیقه — خیلی مهم!)

دکمه «بازسازی دانش» پنل → `reindex_all()` در `backend/app/modules/ai/indexer.py` → خط اولش `delete(RagChunk)` است یعنی **همه chunk ها را پاک می‌کند**. اگر این را نبندید، اولین باری که ادمین بعد از ایندکس کتاب‌ها reindex بزند، **هر ۴۳ کتاب از حافظه چت‌بات پاک می‌شود** و باید ساعت‌ها دوباره ایندکس شود!

```python
# در reindex_all() این خط:
await self.db.execute(delete(RagChunk))
# را به این تبدیل کنید (کتاب‌ها دست نخورند):
await self.db.execute(delete(RagChunk).where(RagChunk.source_type != "book"))
```

## گام ۳ — اسکریپت ایندکس کتاب‌ها: فایل جدید `backend/jobs/index_books.py` (۱ روز)

منطق: هر کتاب → صفحه‌به‌صفحه با `pdftotext` → نرمال‌سازی NFKC → هر صفحه یک chunk با شماره صفحه (صفحه = واحد ذکر منبع!) → امبدینگ با همان `embed_passage` موجود → insert.

```python
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

BOOKS_DIR = Path(__file__).parent.parent.parent / "books"

# نام فایل → (نام دری کتاب، صنف)
BOOK_INFO = {
    "G10-Dr-Math.pdf": ("ریاضی", "10"), "G10-Dr-physic.pdf": ("فزیک", "10"),
    "G10-Dr-Chemistry.pdf": ("کیمیا", "10"), "G10-Dr-Biology.pdf": ("بیولوژی", "10"),
    "G10-Dr-Dari.pdf": ("دری", "10"), "G10-Dr-Pashto.pdf": ("پشتو", "10"),
    "G10-Ps-English.pdf": ("انگلیسی", "10"), "G10-Dr-History.pdf": ("تاریخ", "10"),
    "G10-Dr-Geography.pdf": ("جغرافیه", "10"), "G10-Dr-Geology.pdf": ("جیولوژی", "10"),
    "G10-Dr-Civic.pdf": ("تعلیمات مدنی", "10"), "G10-Dr-Computer.pdf": ("کمپیوتر", "10"),
    "G10-Dr-Islamic_Study_hanafi.pdf": ("تعلیمات اسلامی (حنفی)", "10"),
    "G10-Dr-Islamic_Study_jafari.pdf": ("تعلیمات اسلامی (جعفری)", "10"),
    "G10-Dr-Tafseer.pdf": ("تفسیر شریف", "10"),
    # صنف ۱۱ و ۱۲ را به همین شکل کامل کنید (نام فایل‌ها در بخش ۲ book.md)
}

MIN_CHARS = 200  # صفحات خیلی کوتاه (جلد، سفید) رد شوند


def extract_page(pdf: Path, page: int) -> str:
    out = subprocess.run(
        ["pdftotext", "-f", str(page), "-l", str(page), str(pdf), "-"],
        capture_output=True, text=True, timeout=30,
    ).stdout
    # ⚠️ حیاتی: حروف نمایشی عربی (ﻣﻰتﻮاﻧﻴد) → حروف استاندارد (می‌توانید)
    return unicodedata.normalize("NFKC", out).strip()


def page_count(pdf: Path) -> int:
    info = subprocess.run(["pdfinfo", str(pdf)], capture_output=True, text=True).stdout
    return int(next(l for l in info.splitlines() if l.startswith("Pages")).split()[-1])


async def index_book(db, filename: str):
    book_name, grade = BOOK_INFO[filename]
    pdf = BOOKS_DIR / filename

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
            id=uuid.uuid4(), source_type="book", content=content,
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
    targets = [sys.argv[1]] if len(sys.argv) > 1 else list(BOOK_INFO.keys())
    async with SessionLocal() as db:
        total = 0
        for f in targets:
            total += await index_book(db, f)
        print(f"\nتمام: {total} chunk جدید")

asyncio.run(main())
```

**نکات برای توسعه‌دهنده:**
- `RagChunk.meta["file"].as_string()` = فیلتر JSON در PostgreSQL — اگر خطا داد، ساده‌ترش کنید: قبل از شروع، همه فایل‌های ایندکس‌شده را یکجا `select distinct meta->>'file'` بگیرید.
- زمان تخمینی: ~۹,۰۰۰ صفحه × امبدینگ CPU ≈ **۳۰-۹۰ دقیقه یک‌بار برای همیشه**. شب اجرا کنید یا با `nohup`.
- اول **فقط یک کتاب** تست کنید: `python jobs/index_books.py G10-Dr-physic.pdf` → بعد چک: `SELECT count(*) FROM rag_chunks WHERE source_type='book';`

## گام ۴ — retriever با فیلتر حالت (نیم ساعت)

**فایل `backend/app/modules/ai/retriever.py`** — متد `retrieve` را گسترش دهید:
```python
    async def retrieve(self, question: str, limit: int = 8, source_types: list[str] | None = None):
        q_emb = embed_query(question)
        q = select(RagChunk.content, RagChunk.meta)
        if source_types:
            q = q.where(RagChunk.source_type.in_(source_types))
        q = q.order_by(RagChunk.embedding.cosine_distance(q_emb)).limit(limit)
        rows = (await self.db.execute(q)).all()
        return [(r[0], r[1]) for r in rows]   # (content, meta)
```
⚠️ جاهای دیگری که `retrieve` صدا زده می‌شود (ai/service.py) خروجی جدید tuple است — آپدیت کنید.

## گام ۵ — حالت «سوال از کتاب درسی» در چت (۱ روز)

**فایل `backend/app/modules/ai/service.py`:**
```python
BOOK_SYSTEM_PROMPT = """تو معلم کتاب‌های درسی رسمی وزارت معارف افغانستان هستی.
فقط و فقط از «متن کتاب‌ها» که پایین آمده جواب بده — از دانش خودت هیچ چیزی اضافه نکن.
در پایان جواب، منبع را دقیق بنویس: نام کتاب، صنف و صفحه (در سر هر بخش متن آمده).
اگر جواب در متن کتاب‌ها نبود، فقط بنویس:
«پاسخ این سؤال در کتاب‌های درسی موجود نیست.»
به زبان {language} و ساده جواب بده.

=== متن کتاب‌ها ===
{context}"""
```
در `ChatService.ask` پارامتر `mode: str = "general"` اضافه کنید:
- `mode == "books"` → `retriever.retrieve(message, source_types=["book"])` + پرامپت بالا
- در غیر آن → رفتار فعلی (همه منابع)
- ⚠️ کلید کش را هم mode دار کنید (در `cache.py` به `_key` پارامتر mode اضافه شود) وگرنه جواب دو حالت قاطی می‌شود!
- در `router.py` چت، فیلد `mode` به schema ورودی اضافه شود.

**فرانت — `web/app/chat/page.tsx`:** یک toggle بالای چت:
```tsx
<label className="flex items-center gap-2 text-sm text-muted cursor-pointer mb-3">
  <input type="checkbox" checked={booksMode} onChange={e => setBooksMode(e.target.checked)} className="w-4 h-4" />
  📚 فقط از کتاب‌های درسی جواب بده (با ذکر کتاب و صفحه)
</label>
```
و در body درخواست: `mode: booksMode ? "books" : "general"`.

## گام ۶ — تست‌ها (نیم روز)

فایل جدید `backend/app/tests/test_book_rag.py`: ۱) retrieve با فیلتر source_types فقط chunk کتابی برگرداند ۲) endpoint چت با mode=books بدون خطا جواب دهد (اگر Redis/AI در تست نیست، حداقل validation ورودی). + تست دستی بخش ۴.

---

# بخش ۴: تست پذیرش نهایی (دقیقاً همان مثال‌های b.md)

بعد از ایندکس کامل، این ۵ سوال را در حالت «📚 فقط از کتاب درسی» بپرسید:

| # | سوال | جواب قابل قبول |
|---|---|---|
| ۱ | قانون دوم نیوتن چیست؟ | F = ma + **منبع: کتاب فزیک صنف ۱۰، صفحه X** |
| ۲ | پایتخت افغانستان چیست؟ | کابل + منبع از جغرافیه/مدنی |
| ۳ | فعل ماضی چیست؟ | تعریف از کتاب دری + منبع |
| ۴ | هایبریدیزیشن کاربن در ایتلین چگونه است؟ | از کیمیا صنف ۱۲ + منبع |
| ۵ | قیمت بیت‌کوین چند است؟ | دقیقاً: **«پاسخ این سؤال در کتاب‌های درسی موجود نیست.»** |

معیار: ۴ سوال اول با منبع درست (کتاب + صنف + صفحه) · سوال ۵ فقط جمله ردّ استاندارد · هیچ جوابی از «دانش عمومی مدل» نیامده باشد.
این ۵ سوال را به Golden Set (فایل `assist/golden-questions.md` — پلان ۴.۴.ج) هم اضافه کنید.

---

# بخش ۵: ریسک‌ها و جواب‌ها

| ریسک | جواب |
|---|---|
| فرمول‌های ریاضی/کیمیا در استخراج متن به‌هم می‌ریزند | طبیعی است؛ متن توضیحی سالم است و برای RAG کافی. برای فرمول دقیق، شاگرد به صفحه/کتاب ارجاع داده می‌شود (منبع ذکر می‌شود) |
| حق نشر | کتاب‌های رسمی دولتی‌اند و وزارت خودش عمومی منتشر کرده؛ ما هم منبع (کتاب/صفحه) را در هر جواب ذکر می‌کنیم و فایل‌ها را بازنشر نمی‌کنیم (فقط روی سرور خودمان) |
| حجم DB | ~۹-۱۲ هزار chunk × وکتور ۳۸۴بعدی ≈ چند صد MB — برای Postgres هیچ است |
| صفحه PDF ≠ شماره صفحه چاپی کتاب | ممکن است ±۲-۳ صفحه فرق کند (جلد/فهرست) — قابل قبول؛ در UI بنویسید «حدود صفحه X» اگر خواستید دقیق‌تر شود |
| «فصل» در منبع نداریم | فعلاً کتاب+صنف+صفحه کافی است؛ استخراج نام فصل از سرخط‌ها = بهبود آینده |
| reindex پنل کتاب‌ها را پاک کند | گام ۲ همین را می‌بندد — **اول از همه انجامش دهید** |
| ایندکس وسط راه قطع شود | اسکریپت قابل ادامه است (کتاب ایندکس‌شده را رد می‌کند) |

---

# ترتیب اجرا (خلاصه یک‌خطی)

گام ۲ (بستن باگ reindex) → گام ۱ (ستون meta) → گام ۳ با **یک کتاب** تست → گام ۴ و ۵ (retriever + حالت کتاب + toggle چت) → گام ۳ برای هر ۴۳ کتاب (شب) → بخش ۴ (۵ تست پذیرش) → تیک‌های بخش ۲ تکمیل.
