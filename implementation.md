# 🛠️ راهنمای پیاده‌سازی گام‌به‌گام (Implementation Guide)
## پلتفرم راهنمای هوشمند پوهنتون هرات — نسخه وب‌محور

**نسخه:** 1.0
**پیش‌نیاز مطالعه:** سند «نقشه-راه-توسعه-نسخه-۲.md» (محتوای آن به **نسخه ۳.۰ وب-اول** به‌روز شده — معماری، یافته‌های تحقیق بازار و دلایل انتخاب تکنالوژی آنجاست؛ این سند فقط «چگونه ساختن» است)
**مخاطب:** توسعه‌دهنده‌ای که شاید تا حالا سیستم بزرگ ننوشته باشد — هر مرحله دقیقاً می‌گوید چه فایلی بسازد، چه کلاسی بنویسد و چه زمانی مرحله «تمام» حساب می‌شود.

---

# بخش ۰: اصول معماری — قبل از نوشتن حتی یک خط کد بخوانید

این پروژه باید طوری ساخته شود که **تغییر در یک بخش، بخش‌های دیگر را نشکند**. برای رسیدن به این هدف، پنج قانون زیر در تمام پروژه مقدس است:

## قانون ۱: معماری لایه‌ای (Layered Architecture)

هر درخواست (Request) فقط در یک جهت حرکت می‌کند:

```
Router (لایه HTTP)  ←  فقط ورودی را می‌گیرد و خروجی را برمی‌گرداند
   ↓
Service (لایه منطق)  ←  تمام منطق تجاری اینجاست
   ↓
Repository (لایه داده)  ←  تنها جایی که با دیتابیس حرف می‌زند
   ↓
Model (جدول دیتابیس)
```

- **Router هرگز مستقیم به دیتابیس دست نمی‌زند.**
- **Service هرگز کد SQL یا Query ننویسد** — فقط متدهای Repository را صدا می‌زند.
- **Repository هرگز منطق تجاری ندارد** — فقط خواندن/نوشتن.

**چرا؟** اگر فردا دیتابیس عوض شد، فقط Repository ها تغییر می‌کنند. اگر منطق عوض شد، فقط Service. اگر فرمت API عوض شد، فقط Router.

## قانون ۲: هر Feature یک ماژول مستقل (Vertical Slice)

هر قابلیت (رشته‌ها، اخبار، کانکور، AI...) پوشه خودش را دارد با router + service + repository + schema خودش. حذف یک پوشه = حذف تمیز آن قابلیت، بدون شکستن بقیه.

## قانون ۳: قطعات تعویض‌پذیر پشت Interface

هر چیزی که «ممکن است روزی عوض شود» پشت یک کلاس انتزاعی (Abstract Base Class) قرار می‌گیرد:

| قطعه | Interface | پیاده‌سازی امروز | پیاده‌سازی احتمالی فردا |
|---|---|---|---|
| مدل هوش مصنوعی | `AIProvider` | Gemini | OpenRouter / Claude / Ollama |
| ذخیره فایل | `StorageProvider` | دیسک محلی | MinIO / S3 |
| جستجو | `SearchProvider` | PostgreSQL FTS | Meilisearch |
| نوتیفیکیشن | `NotifierProvider` | FCM | ایمیل / تلگرام |

تعویض = نوشتن یک کلاس جدید + تغییر یک خط در `.env`. **هیچ کد دیگری دست نمی‌خورد.**

## قانون ۴: Schema (قرارداد) جدا از Model (جدول)

- `models/` = شکل جدول در دیتابیس (SQLAlchemy)
- `schemas/` = شکل داده در ورودی/خروجی API (Pydantic)

هرگز Model را مستقیم به کلاینت نفرستید. اگر فردا ستونی به جدول اضافه شد، API بیرونی تغییر نمی‌کند مگر خودتان بخواهید.

## قانون ۵: تغییر دیتابیس فقط با Migration

هیچ‌کس دستی جدول نمی‌سازد یا ستون اضافه نمی‌کند. هر تغییر = یک فایل Alembic migration که در Git ثبت می‌شود. این یعنی دیتابیس هر عضو تیم و سرور همیشه هم‌شکل است.

---

# بخش ۱: ساختار کامل مخزن (Monorepo)

یک مخزن Git واحد با این ساختار — **همین امروز این پوشه‌ها را بسازید:**

```
herat-uni-guide/
├── README.md
├── docker-compose.yml          # postgres+pgvector, redis, api, web
├── .env.example                # الگوی متغیرها — هرگز .env واقعی در Git نرود
├── .gitignore
│
├── backend/                    # FastAPI
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── alembic/                # migration ها
│   ├── alembic.ini
│   └── app/
│       ├── main.py             # نقطه شروع — فقط اتصال router ها
│       ├── config.py           # خواندن .env با pydantic-settings
│       ├── database.py         # engine + session + Base
│       │
│       ├── core/               # چیزهای مشترک همه ماژول‌ها
│       │   ├── deps.py         # Dependency های FastAPI (get_db, get_current_admin)
│       │   ├── security.py     # JWT + hash پسورد
│       │   ├── exceptions.py   # خطاهای سفارشی پروژه
│       │   └── pagination.py   # صفحه‌بندی استاندارد
│       │
│       ├── modules/            # ⭐ هر قابلیت = یک پوشه مستقل (قانون ۲)
│       │   ├── universities/
│       │   │   ├── models.py
│       │   │   ├── schemas.py
│       │   │   ├── repository.py
│       │   │   ├── service.py
│       │   │   └── router.py
│       │   ├── faculties/      # همین پنج فایل
│       │   ├── departments/    # همین پنج فایل (+ زیرجدول‌ها)
│       │   ├── news/
│       │   ├── faqs/
│       │   ├── kankor/         # کات‌آف + ماشین حساب چانس + راهنماها
│       │   ├── quiz/           # آزمون انتخاب رشته
│       │   ├── ai/             # چت‌بات RAG
│       │   ├── search/
│       │   ├── notifications/
│       │   └── admin_auth/
│       │
│       ├── providers/          # ⭐ قطعات تعویض‌پذیر (قانون ۳)
│       │   ├── ai/
│       │   │   ├── base.py     # class AIProvider(ABC)
│       │   │   ├── gemini.py
│       │   │   └── openrouter.py
│       │   ├── storage/
│       │   │   ├── base.py     # class StorageProvider(ABC)
│       │   │   ├── local.py
│       │   │   └── minio.py
│       │   └── search/
│       │       ├── base.py
│       │       └── postgres_fts.py
│       │
│       └── tests/              # آینه پوشه modules
│           ├── conftest.py     # دیتابیس تست + کلاینت تست
│           └── test_departments.py, test_kankor.py, ...
│
└── web/                        # Next.js (TypeScript)
    ├── package.json
    └── src/
        ├── app/                # صفحات (App Router)
        │   ├── layout.tsx      # قالب کلی: هدر، فوتر، فونت، RTL
        │   ├── page.tsx        # صفحه اصلی
        │   ├── faculties/
        │   │   ├── page.tsx                # لیست پوهنځی‌ها
        │   │   ├── [slug]/page.tsx         # صفحه پوهنځی: دیدگاه/ماموریت + دو بخش جدا
        │   │   │                           #   (رشته‌های فارغ‌ده / دیپارتمنت‌های خدماتی)
        │   │   └── [slug]/[dept]/page.tsx  # ⭐ صفحه غنی رشته — URL سلسله‌مراتبی
        │   │                               #   (سئو بهتر + breadcrumb طبیعی)
        │   ├── kankor/
        │   │   ├── page.tsx            # راهنمای کانکور
        │   │   └── chance/page.tsx     # ⭐ ماشین حساب چانس
        │   ├── quiz/page.tsx           # آزمون انتخاب رشته
        │   ├── chat/page.tsx           # چت‌بات AI
        │   └── news/...
        │
        ├── components/         # قطعات UI قابل استفاده مجدد
        │   ├── ui/             # Button, Card, Input, Badge ...
        │   ├── layout/         # Header, Footer, Sidebar
        │   └── features/       # DepartmentCard, ChanceResult, ChatBubble ...
        │
        ├── lib/
        │   ├── api.ts          # ⭐ تنها جای صدا زدن Backend
        │   ├── types.ts        # Type های TypeScript (آینه schemas بک‌اند)
        │   └── i18n/           # دیکشنری سه زبان fa/ps/en
        │
        └── styles/
```

**قانون طلایی فرانت‌اند:** هیچ کامپوننتی مستقیم `fetch` نمی‌زند — همه از توابع `lib/api.ts` استفاده می‌کنند. اگر آدرس یا فرمت API عوض شد، فقط یک فایل تغییر می‌کند.

---

# بخش ۲: فازبندی — نمای کلی

| فاز | نام | مدت تقریبی | خروجی قابل نمایش |
|---|---|---|---|
| ۰ | زیرساخت و اسکلت | ۱ هفته | `docker compose up` → سه سرویس بالا |
| ۱ | هسته محتوایی Backend | ۳ هفته | API کامل رشته‌ها با داده واقعی CS در Swagger |
| ۲ | وبسایت عمومی | ۳ هفته | سایت سه‌زبانه با صفحه غنی رشته، آنلاین |
| ۳ | کانکور + ماشین حساب چانس + آزمون رشته | ۲ هفته | شاگرد نمره تخمینی بزند → چانس ببیند |
| ۴ | هوش مصنوعی (RAG + چت) | ۳ هفته | چت‌بات دری که از داده واقعی سایت جواب بدهد |
| ۵ | پنل ادمین + نوتیفیکیشن | ۲ هفته | مسئول محتوا بدون برنامه‌نویس محتوا وارد کند |
| ۶ | استقرار عمومی + سئو | ۱ هفته | دامنه واقعی، HTTPS، ایندکس گوگل |

هر فاز «تعریف تمام‌شدن» (Definition of Done) دارد — تا چک‌لیست آن سبز نشود، فاز بعدی شروع نمی‌شود.

---

# فاز ۰: زیرساخت و اسکلت (هفته ۱)

## مرحله ۰.۱ — مخزن و Docker

1. `git init` + ساخت ساختار پوشه بخش ۱ (پوشه‌های خالی با فایل `.gitkeep`)
2. `docker-compose.yml` با سه سرویس:

```yaml
services:
  db:
    image: pgvector/pgvector:pg16
    environment:
      POSTGRES_DB: uniguide
      POSTGRES_USER: uniguide
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes: ["pgdata:/var/lib/postgresql/data"]
    ports: ["5432:5432"]
  redis:
    image: redis:7-alpine
  api:
    build: ./backend
    env_file: .env
    depends_on: [db, redis]
    ports: ["8000:8000"]
volumes:
  pgdata:
```

3. `.env.example` (کپی آن `.env` می‌شود، `.env` در `.gitignore`):

```
DB_PASSWORD=change-me
DATABASE_URL=postgresql+asyncpg://uniguide:change-me@db:5432/uniguide
REDIS_URL=redis://redis:6379/0
JWT_SECRET=change-me-long-random
AI_PROVIDER=gemini
AI_MODEL=gemini-2.5-flash
AI_API_KEY=
STORAGE_PROVIDER=local
```

## مرحله ۰.۲ — اسکلت Backend

`requirements.txt`:

```
fastapi
uvicorn[standard]
sqlalchemy[asyncio]>=2.0
asyncpg
alembic
pydantic-settings
python-jose[cryptography]
passlib[bcrypt]
redis
httpx
pillow
sentence-transformers
pgvector
pytest
pytest-asyncio
```

**`app/config.py`** — تنها جای خواندن تنظیمات:

```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str
    redis_url: str
    jwt_secret: str
    ai_provider: str = "gemini"
    ai_model: str = "gemini-2.5-flash"
    ai_api_key: str = ""
    storage_provider: str = "local"

    class Config:
        env_file = ".env"

settings = Settings()
```

**`app/database.py`**:

```python
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from app.config import settings

engine = create_async_engine(settings.database_url)
SessionLocal = async_sessionmaker(engine, expire_on_commit=False)

class Base(DeclarativeBase):
    pass
```

**`app/core/deps.py`**:

```python
from app.database import SessionLocal

async def get_db():
    async with SessionLocal() as session:
        yield session
```

**`app/main.py`** — فقط سرهم‌بندی، هیچ منطقی اینجا نوشته نمی‌شود:

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Herat University Guide API", version="1.0")

app.add_middleware(CORSMiddleware, allow_origins=["http://localhost:3000"],
                   allow_methods=["*"], allow_headers=["*"])

@app.get("/health")
async def health():
    return {"status": "ok"}

# با اضافه شدن هر ماژول، یک خط اینجا اضافه می‌شود:
# from app.modules.departments.router import router as departments_router
# app.include_router(departments_router, prefix="/api/v1")
```

4. راه‌اندازی Alembic: `alembic init alembic` و در `env.py` آن `Base.metadata` را وصل کنید.

## مرحله ۰.۳ — اسکلت Web

```bash
npx create-next-app@latest web --typescript --tailwind --app
```

- در `layout.tsx`: `dir="rtl"`، فونت **Vazirmatn Variable** به‌صورت self-hosted با `next/font/local`
- کپی توکن‌های رنگ مرحله ۲.۲.۲ در `tailwind.config.ts` — از روز اول، حتی برای صفحه تست
- ⭐ پروتوتایپ بصری سه صفحه کلیدی (اصلی، رشته، چانس) — Figma یا HTML استاتیک با همین توکن‌ها → تایید Product Owner (مرحله ۲.۲.۷)
- `lib/api.ts` اولیه:

```typescript
const BASE = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000/api/v1";

async function get<T>(path: string): Promise<T> {
  const res = await fetch(`${BASE}${path}`, { next: { revalidate: 300 } });
  if (!res.ok) throw new Error(`API ${res.status}: ${path}`);
  return res.json();
}

export const api = { get };
```

## ✅ تعریف تمام‌شدن فاز ۰

- [ ] `docker compose up` بدون خطا؛ `http://localhost:8000/health` جواب `{"status":"ok"}`
- [ ] `http://localhost:8000/docs` (Swagger خودکار) باز می‌شود
- [ ] `npm run dev` در `web/` → صفحه RTL با فونت فارسی
- [ ] `alembic upgrade head` بدون خطا اجرا می‌شود
- [ ] همه چیز در Git، `.env` در Git نیست

---

# فاز ۱: هسته محتوایی Backend (هفته ۲–۴)

## الگوی استاندارد ماژول — یک بار یاد بگیرید، ده بار تکرار کنید

هر ماژول دقیقاً پنج فایل دارد. ماژول `departments` را کامل نشان می‌دهیم؛ بقیه ماژول‌ها **همین الگو** با جدول خودشان هستند.

### `modules/departments/models.py`

```python
import uuid
from datetime import datetime
from sqlalchemy import String, Text, Integer, ForeignKey, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base

class Department(Base):
    __tablename__ = "departments"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    faculty_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("faculties.id"))
    slug: Mapped[str] = mapped_column(String(100), unique=True, index=True)

    # سه‌زبانه: دری اجباری، بقیه اختیاری
    name_fa: Mapped[str] = mapped_column(String(200))
    name_ps: Mapped[str | None] = mapped_column(String(200))
    name_en: Mapped[str | None] = mapped_column(String(200))
    description_fa: Mapped[str] = mapped_column(Text)
    description_ps: Mapped[str | None] = mapped_column(Text)
    description_en: Mapped[str | None] = mapped_column(Text)

    # ⭐ سلسله‌مراتب واقعی: 'degree' = فارغ‌ده (قابل انتخاب در کانکور)
    #                       'service' = خدماتی/غیرفارغ‌ده (مثل «آموزش کامپیوتر» در CS)
    department_type: Mapped[str] = mapped_column(String(10), default="degree", index=True)
    vision_fa: Mapped[str | None] = mapped_column(Text)   # دیدگاه مختص دیپارتمنت
    mission_fa: Mapped[str | None] = mapped_column(Text)  # ماموریت مختص دیپارتمنت

    duration_years: Mapped[int] = mapped_column(Integer, default=4)
    degree_type: Mapped[str] = mapped_column(String(50), default="لیسانس")
    subjects: Mapped[list] = mapped_column(JSON, default=list)        # مضامین اصلی
    career_paths: Mapped[list] = mapped_column(JSON, default=list)    # مسیرهای شغلی
    required_skills: Mapped[list] = mapped_column(JSON, default=list)
    suitable_for: Mapped[list] = mapped_column(JSON, default=list)    # مناسب چه کسی
    job_market_fa: Mapped[str | None] = mapped_column(Text)

    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.utcnow,
                                                 onupdate=datetime.utcnow)

    faculty = relationship("Faculty", back_populates="departments")
    cutoffs = relationship("KankorCutoff", back_populates="department")
```

### `modules/departments/schemas.py`

```python
import uuid
from pydantic import BaseModel, ConfigDict

class DepartmentListItem(BaseModel):
    """برای لیست‌ها — سبک"""
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    slug: str
    name_fa: str
    name_en: str | None
    degree_type: str

class DepartmentDetail(DepartmentListItem):
    """برای صفحه غنی رشته — کامل"""
    description_fa: str
    duration_years: int
    subjects: list
    career_paths: list
    required_skills: list
    suitable_for: list
    job_market_fa: str | None

class DepartmentCreate(BaseModel):
    """ورودی ادمین — id و تاریخ‌ها را سرور می‌سازد"""
    faculty_id: uuid.UUID
    slug: str
    name_fa: str
    description_fa: str
    # ... بقیه فیلدها اختیاری با مقدار پیش‌فرض

class DepartmentUpdate(BaseModel):
    """همه فیلدها اختیاری — فقط فیلدهای فرستاده‌شده آپدیت می‌شوند"""
    name_fa: str | None = None
    description_fa: str | None = None
    # ...
```

### `modules/departments/repository.py`

```python
import uuid
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from .models import Department

class DepartmentRepository:
    """تنها نقطه تماس با دیتابیس برای رشته‌ها (قانون ۱)"""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def list_all(self, faculty_id: uuid.UUID | None = None,
                       department_type: str | None = None) -> list[Department]:
        q = select(Department).order_by(Department.name_fa)
        if faculty_id:
            q = q.where(Department.faculty_id == faculty_id)
        if department_type:  # 'degree' → فقط فارغ‌ده‌ها (چانس، آزمون، مقایسه)
            q = q.where(Department.department_type == department_type)
        return list((await self.db.execute(q)).scalars())

    async def get_by_slug(self, slug: str) -> Department | None:
        q = select(Department).where(Department.slug == slug)
        return (await self.db.execute(q)).scalar_one_or_none()

    async def create(self, data: dict) -> Department:
        obj = Department(**data)
        self.db.add(obj)
        await self.db.commit()
        await self.db.refresh(obj)
        return obj

    async def update(self, obj: Department, data: dict) -> Department:
        for key, value in data.items():
            setattr(obj, key, value)
        await self.db.commit()
        await self.db.refresh(obj)
        return obj

    async def delete(self, obj: Department) -> None:
        await self.db.delete(obj)
        await self.db.commit()
```

### `modules/departments/service.py`

```python
import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.exceptions import NotFoundError
from .repository import DepartmentRepository
from .schemas import DepartmentCreate, DepartmentUpdate

class DepartmentService:
    """منطق تجاری — Router فقط با این کلاس حرف می‌زند"""

    def __init__(self, db: AsyncSession):
        self.repo = DepartmentRepository(db)

    async def list_departments(self, faculty_id: uuid.UUID | None = None):
        return await self.repo.list_all(faculty_id)

    async def get_department(self, slug: str):
        dept = await self.repo.get_by_slug(slug)
        if dept is None:
            raise NotFoundError(f"رشته «{slug}» یافت نشد")
        return dept

    async def create_department(self, payload: DepartmentCreate):
        return await self.repo.create(payload.model_dump())

    async def update_department(self, slug: str, payload: DepartmentUpdate):
        dept = await self.get_department(slug)
        # exclude_unset: فقط فیلدهایی که واقعاً فرستاده شده‌اند
        return await self.repo.update(dept, payload.model_dump(exclude_unset=True))
```

### `modules/departments/router.py`

```python
import uuid
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.deps import get_db
from .service import DepartmentService
from .schemas import DepartmentListItem, DepartmentDetail

router = APIRouter(prefix="/departments", tags=["departments"])

@router.get("", response_model=list[DepartmentListItem])
async def list_departments(faculty_id: uuid.UUID | None = None,
                           db: AsyncSession = Depends(get_db)):
    return await DepartmentService(db).list_departments(faculty_id)

@router.get("/{slug}", response_model=DepartmentDetail)
async def get_department(slug: str, db: AsyncSession = Depends(get_db)):
    return await DepartmentService(db).get_department(slug)
```

### `core/exceptions.py` — خطای یکدست در کل پروژه

```python
class NotFoundError(Exception):
    def __init__(self, message: str):
        self.message = message

# در main.py یک handler سراسری:
# @app.exception_handler(NotFoundError)
# async def not_found_handler(request, exc):
#     return JSONResponse(status_code=404, content={"detail": exc.message})
```

## مراحل فاز ۱ به ترتیب

| مرحله | کار | نکته |
|---|---|---|
| ۱.۱ | ماژول `universities` (همان الگوی ۵ فایلی) | ساده‌ترین — تمرین الگو |
| ۱.۲ | ماژول `faculties` | رابطه با university |
| ۱.۳ | ماژول `departments` + جداول فرعی (`student_projects`, `alumni_stories`, `career_roadmaps`) | جداول فرعی داخل همین ماژول، فایل `models.py` مشترک |
| ۱.۴ | ماژول `news` و `faqs` | تکرار الگو |
| ۱.۵ | migration ها: بعد از هر ماژول `alembic revision --autogenerate` + `alembic upgrade head` | یک migration در هر مرحله |
| ۱.۶ | اسکریپت `seed.py`: ⭐ هر ۱۶ پوهنځی با «پروفایل پایه» + پوهنځی کمپیوتر ساینس با «پروفایل کامل» (الگو) | مهم‌ترین قدم — بدون داده واقعی هیچ چیز قابل تست نیست؛ هیچ پوهنځی‌ای خالی نماند |
| ۱.۷ | تست: برای هر ماژول حداقل ۳ تست (list، get موفق، get ناموجود=404) | pytest + دیتابیس تست جدا |

### الگوی تست (`tests/test_departments.py`)

```python
import pytest

@pytest.mark.asyncio
async def test_get_department_found(client, seed_cs_department):
    res = await client.get("/api/v1/departments/computer-science")
    assert res.status_code == 200
    assert res.json()["name_fa"] == "کمپیوتر ساینس"

@pytest.mark.asyncio
async def test_get_department_not_found(client):
    res = await client.get("/api/v1/departments/nonexistent")
    assert res.status_code == 404
```

## ⭐ پوشش هر ۱۶ پوهنځی — قالب استاندارد و سه موج محتوا

معماری از اول چند-پوهنځی است — پوشش کامل مسئله **کد نیست، محتواست.** راه‌حل: دو سطح محتوا + سه موج تکمیل.

### فهرست ۱۶ پوهنځی — تایید شده از صفحه معرفی رسمی: «۱۶ پوهنځی و ۷۰ دیپارتمنت» (نام دقیق دری هنگام هماهنگی تایید شود)

طب · ستوماتولوژی · انجنیری · کمپیوتر ساینس · اقتصاد · حقوق و علوم سیاسی · تعلیم و تربیه · ساینس · زراعت · علوم وترنری · ادبیات و علوم بشری · ژورنالیزم · شرعیات · هنرها · علوم اجتماعی · اداره و پالیسی عامه

### دو سطح محتوا

| سطح | شامل | زحمت تقریبی | کِی |
|---|---|---|---|
| **پروفایل پایه** | نام + معرفی ۲ پاراگراف + ⭐ فهرست دیپارتمنت‌ها با **نوع هر کدام (فارغ‌ده/خدماتی)** + دیدگاه و ماموریت هر دیپارتمنت + مدت و مدرک + مضامین کلیدی + ۳ مسیر شغلی + کات‌آف سال‌های موجود | ~نیم روز برای هر پوهنځی (مجموع ۷۰ دیپارتمنت — واحد کار «رشته» است) | همه ۱۶ تا در فاز ۱ (داخل `seed.py`) |
| **پروفایل کامل** | پایه + پروژه‌های دانشجویی + داستان/مصاحبه فارغان + Career Roadmap + FAQ اختصاصی + عکس‌های واقعی + استادان | ~۳-۵ روز برای هر پوهنځی | CS در فاز ۱ (الگو)؛ بقیه در سه موج |

**قانون UI:** صفحه پوهنځی با پروفایل پایه هم باید کامل و زیبا دیده شود — بخش‌های خالی اصلاً render نشوند (نه `EmptyState` زشت وسط صفحه، نه بخش خالی). محتوا که رسید، بخش خودکار ظاهر می‌شود.

### سه موج تکمیل (بر اساس تقاضای کانکور)

| موج | پوهنځی‌ها | زمان |
|---|---|---|
| ۱ — پرمتقاضی | طب، ستوماتولوژی، انجنیری، اقتصاد، حقوق، تعلیم و تربیه (+ CS که الگوست) | موازی فازهای ۲-۳ |
| ۲ | ساینس، زراعت، وترنری، ژورنالیزم، اداره و پالیسی عامه | موازی فازهای ۴-۵ |
| ۳ | ادبیات، هنرها، شرعیات، علوم اجتماعی | قبل یا کمی بعد از انتشار |

### گردش کار جمع‌آوری (با شبکه رابط‌ها)

1. یک **فورم استاندارد** (Google Form یا سند Word) دقیقاً با فیلدهای «پروفایل پایه/کامل» ساخته شود — رابط هر پوهنځی پر می‌کند. ⭐ اولین سوال فورم: «پوهنځی شما چند دیپارتمنت دارد؟ کدام‌ها فارغ‌ده و کدام‌ها خدماتی؟ دیدگاه و ماموریت هر کدام؟» (سایت رسمی این جزئیات را ندارد — تنها منبع معتبر خود پوهنځی‌هاست)
2. مسئول محتوا: ویرایش، یکدست‌سازی لحن، ترجمه پشتو/انگلیسی
3. رابط پوهنځی صحت علمی را تایید می‌کند → ورود به سیستم → ثبت `reviewed_by` و تاریخ
4. بعد از هر ورود: Reindex RAG — چت‌بات فوراً پوهنځی جدید را «یاد می‌گیرد»

## ✅ تعریف تمام‌شدن فاز ۱

- [ ] در Swagger: universities، faculties، departments، news، faqs همه کار می‌کنند
- [ ] `python seed.py` → ⭐ هر ۱۶ پوهنځی با پروفایل پایه در دیتابیس + پوهنځی CS کامل با ساختار واقعی: ۳ دیپارتمنت فارغ‌ده (دیتابیس/سیستم‌های معلوماتی، نتورک/تکنالوژی معلوماتی، انجنیری نرم‌افزار — هر کدام با دیدگاه/ماموریت/مسیر شغلی مختص خود) + ۱ دیپارتمنت خدماتی (آموزش کامپیوتر با `department_type='service'`)
- [ ] فورم استاندارد محتوا ساخته و به رابط‌های موج ۱ فرستاده شده
- [ ] `pytest` سبز — حداقل ۱۵ تست
- [ ] هیچ Query دیتابیس بیرون از Repository ها نیست (بازبینی کد)

---

# فاز ۲: وبسایت عمومی (هفته ۵–۷)

## مرحله ۲.۱ — لایه API و Type ها

`lib/types.ts` — آینه دقیق schemas بک‌اند:

```typescript
export interface DepartmentListItem {
  id: string;
  slug: string;
  name_fa: string;
  name_en: string | null;
  degree_type: string;
}

export interface DepartmentDetail extends DepartmentListItem {
  description_fa: string;
  duration_years: number;
  subjects: string[];
  career_paths: CareerPath[];
  required_skills: string[];
  suitable_for: string[];
  job_market_fa: string | null;
}
```

`lib/api.ts` — برای هر ماژول یک گروه تابع:

```typescript
export const api = {
  departments: {
    list: (facultyId?: string) =>
      get<DepartmentListItem[]>(`/departments${facultyId ? `?faculty_id=${facultyId}` : ""}`),
    get: (slug: string) => get<DepartmentDetail>(`/departments/${slug}`),
  },
  faculties: { /* ... */ },
  news: { /* ... */ },
};
```

## مرحله ۲.۲ — ⭐ سیستم دیزاین (Design System) — قبل از ساخت هر صفحه

ظاهر حرفه‌ای اتفاقی نیست — نتیجه سیستم است. اول توکن‌ها، بعد کامپوننت‌ها، بعد صفحات. **هرگز برعکس.**

### ۲.۲.۱ — هویت بصری: «کاشی هراتی»

الهام از کاشی‌کاری مسجد جامع هرات: **لاجوردی** (اعتماد، دانشگاه) + **فیروزه‌ای** (تازگی) + **طلایی** (افتخار، CTA ویژه). این هویت یکتاست — سایت شبیه هیچ قالب آماده‌ای نمی‌شود.

### ۲.۲.۲ — توکن‌های رنگ (`tailwind.config.ts`)

```typescript
// extend.colors — تنها منبع رنگ در کل پروژه
colors: {
  primary: {   // لاجوردی — برند اصلی
    50: "#EEF4FB", 100: "#D9E6F6", 200: "#B3CDEC", 300: "#84ADDF",
    400: "#4F86CD", 500: "#2D66B5", 600: "#1E5AA8", 700: "#174683",
    800: "#123763", 900: "#0D2848",
  },
  accent: { 400: "#2BBFB9", 500: "#12A5A0", 600: "#0E8783" }, // فیروزه‌ای — لینک، تاکید
  gold:   { 400: "#F5B841", 500: "#E0A22E", 600: "#C4871C" }, // طلایی — CTA ویژه، ستاره
  success: "#16A34A",   // چانس بالا
  warning: "#D97706",   // چانس متوسط
  danger:  "#DC2626",   // چانس پایین
  surface: {            // پس‌زمینه‌ها — دو حالت
    light: "#F8FAFC", "light-card": "#FFFFFF",
    dark: "#0B1220",  "dark-card": "#111C30",
  },
}
```

**سه قانون رنگ:**
1. **هیچ کد hex در هیچ کامپوننتی** — فقط نام توکن (`bg-primary-600`). تغییر سلیقه فردا = تغییر config، نه کد.
2. متن روی `primary-600` به پایین همیشه سفید — کنتراست ۴.۵:۱ رعایت شود (با ابزار contrast checker تست کنید).
3. رنگ چانس (سبز/زرد/سرخ) **هرگز تنها حامل معنا نباشد** — همیشه با متن («چانس بالا») و آیکن. کاربر کوررنگ هم باید بفهمد.

### ۲.۲.۳ — تایپوگرافی

- فونت: **Vazirmatn Variable** — self-hosted با `next/font/local` (نه Google Fonts — تحریم/سرعت). برای EN همان کافی است.
- مقیاس: `h1: 30px/بولد` · `h2: 24px` · `h3: 20px` · `body: 16px` · `small: 14px` — موبایل یک پله کوچک‌تر.
- `line-height` متن فارسی: **1.8** (فارسی جای بیشتری نفس می‌خواهد).
- اعداد و تاریخ همه‌جا فارسی/شمسی از یک تابع کمکی:

```typescript
// lib/format.ts — تنها جای فرمت اعداد و تاریخ
export const formatNumber = (n: number) =>
  new Intl.NumberFormat("fa-AF").format(n);
export const formatDateShamsi = (iso: string) =>
  new Intl.DateTimeFormat("fa-AF-u-ca-persian", { dateStyle: "long" })
    .format(new Date(iso));
```

### ۲.۲.۴ — سطح‌ها و فاصله‌ها

- گردی گوشه: دکمه `10px`، کارت `16px`، ورودی `10px` — همه‌جا یکسان.
- سایه کارت: نرم و دولایه (`shadow-sm` پیش‌فرض، `shadow-md` روی hover) — نه سایه سیاه سنگین.
- فاصله‌ها فقط مضرب ۴ (`p-4`, `gap-6`...) — چشم نظم را حس می‌کند حتی اگر نفهمد چرا.
- Dark Mode: استراتژی `class` در Tailwind + توکن‌های `surface.dark`؛ در حالت تیره primary یک پله روشن‌تر (`primary-400`) تا کنتراست حفظ شود.

### ۲.۲.۵ — کامپوننت‌های پایه (`components/ui/`) با Variant ها

| کامپوننت | Variant / State ها |
|---|---|
| `Button` | `primary` / `outline` / `gold` (فقط CTA اصلی صفحه) / `ghost` + حالت‌های `loading`, `disabled` — ارتفاع موبایل ≥ 44px |
| `Card` | ساده / کلیک‌پذیر (hover: سایه + حرکت ۲px بالا) |
| `Badge` | `success` / `warning` / `danger` / `neutral` — برای چانس و برچسب‌ها |
| `ChanceMeter` | نمایش چانس: رنگ + آیکن + متن + نوار درصدی |
| `StatCard` | عدد بزرگ + برچسب (آمار دانشگاه، کات‌آف) |
| `Stepper` | عمودی — Career Roadmap |
| `SectionTitle` | عنوان بخش با خط تزئینی طلایی کوچک |
| `LangSwitcher` | سه زبان — همیشه در هدر |
| `LoadingSkeleton` | برای هر لیست و کارت — هرگز صفحه سفید خالی |
| `EmptyState` | آیکن + پیام دوستانه + پیشنهاد اقدام («هنوز خبری نیست») |

**قانون:** صفحات فقط از این کامپوننت‌ها ساخته می‌شوند. اگر صفحه‌ای چیز جدیدی خواست، اول به `ui/` اضافه می‌شود بعد استفاده — کپی-پیست استایل ممنوع.

### ۲.۲.۶ — قوانین UX (برای کاربر واقعی افغانستان)

1. **موبایل-اول:** طراحی از عرض ۳۶۰px شروع می‌شود؛ دسکتاپ گسترش آن است، نه برعکس.
2. **بودجه سرعت (اینترنت 3G):** تصاویر WebP + `loading="lazy"`، فونت subset‌شده، صفحه اصلی زیر ~۲۰۰KB انتقال اولیه. سایت کند = کاربر برنمی‌گردد.
3. **هیچ لحظه «مرده»:** هر عمل async → skeleton یا spinner؛ هر خطا → پیام دری دوستانه + دکمه تلاش مجدد؛ هر لیست خالی → `EmptyState`.
4. **لمس راحت:** هدف لمسی ≥ 44px، فرم‌ها تک‌ستونه، خطای فرم زیر همان فیلد به دری.
5. **RTL کامل:** آیکن‌های جهت‌دار (فلش‌ها) در RTL آینه شوند؛ در هر PR یک اسکرین‌شات موبایل الزامی.

### ۲.۲.۷ — فرایند: اول پروتوتایپ، بعد کد

قبل از کدنویسی صفحات، **سه صفحه کلیدی** (اصلی، صفحه غنی رشته، ماشین حساب چانس) پروتوتایپ شوند — Figma یا حتی یک HTML استاتیک با همین توکن‌ها. Product Owner تایید کند، بعد ساخت شروع شود. تغییر سلیقه بعد از تایید = فقط توکن‌ها عوض می‌شوند، کامپوننت‌ها نه.

## مرحله ۲.۳ — صفحات به ترتیب اولویت

1. **صفحه اصلی:** بنر + «رشته مناسبت را پیدا کن» (لینک آزمون) + «چانست را حساب کن» (لینک ماشین حساب) + پوهنځی‌ها + آخرین اخبار
2. **⭐ صفحه غنی رشته** (`faculties/[slug]/[dept]/page.tsx`) — مهم‌ترین صفحه سایت. Server Component (برای سئو) با بخش‌ها: breadcrumb (پوهنتون ← پوهنځی ← دیپارتمنت)، دیدگاه و ماموریت مختص دیپارتمنت، معرفی، مضامین، ⭐ بخش «این رشته با رشته‌های همسایه چه فرق دارد؟» (تمایز شغلی — فارغ دیتابیس ≠ فارغ نتورک ≠ فارغ انجنیری نرم‌افزار)، آینده شغلی، مهارت‌ها، «مناسب چه کسی است»، پروژه‌های دانشجویی، داستان فارغان، کات‌آف سال‌های قبل، Career Roadmap (stepper عمودی)
3. **صفحه پوهنځی — سلسله‌مراتب شفاف:** دیدگاه/ماموریت پوهنځی، سپس دو بخش کاملاً جدا: ⭐ «رشته‌های فارغ‌ده» (کارت‌های بزرگ + Badge «قابل انتخاب در کانکور») و «دیپارتمنت‌های خدماتی» (بخش کوچک‌تر + توضیح: «این دیپارتمنت خدمات آموزشی می‌دهد و در کانکور انتخاب نمی‌شود»). شاگرد هرگز دیپارتمنت خدماتی را رشته کانکوری فکر نکند.
4. اخبار + صفحه خبر
5. FAQ (آکاردئون با جستجوی سمت کلاینت)

## مرحله ۲.۴ — سه‌زبانگی

- `lib/i18n/fa.ts`, `ps.ts`, `en.ts` — دیکشنری متن‌های ثابت UI
- متن‌های محتوایی از خود API می‌آیند (فیلدهای `_fa/_ps/_en`)
- یک تابع کمکی: `pickLang(obj, "name", lang)` → اگر ترجمه نبود، به دری برگردد (fallback)
- زبان در URL: `/`، `/ps/...`، `/en/...` — برای سئو بهتر از کوکی است

## مرحله ۲.۵ — سئو (دلیل اصلی وب‌محور بودن!)

- هر صفحه: `generateMetadata` با عنوان و توضیح دری
- `sitemap.ts` خودکار از لیست رشته‌ها و اخبار
- داده ساختاریافته `JSON-LD` نوع `CollegeOrUniversity` در صفحه اصلی

## ✅ تعریف تمام‌شدن فاز ۲

- [ ] صفحه رشته CS با تمام بخش‌ها و داده واقعی، در موبایل و دسکتاپ درست نمایش می‌یابد
- [ ] ⭐ صفحه هر ۱۶ پوهنځی باز می‌شود و با «پروفایل پایه» هم کامل و زیبا دیده می‌شود (بخش بی‌محتوا render نشود)
- [ ] ⭐ صفحه پوهنځی CS: دو بخش جدای فارغ‌ده/خدماتی درست نمایش می‌یابد؛ breadcrumb در صفحه رشته کار می‌کند؛ بخش «تمایز با رشته‌های همسایه» در هر ۳ رشته فارغ‌ده پر است
- [ ] سوییچ سه زبان کار می‌کند، fallback به دری درست است
- [ ] Lighthouse: Performance، SEO و Accessibility بالای ۹۰
- [ ] هیچ `fetch` مستقیمی بیرون از `lib/api.ts` نیست
- [ ] هیچ کد hex رنگ بیرون از `tailwind.config.ts` نیست (جستجوی `#` در پوشه components)
- [ ] Dark Mode در همه صفحات سالم است
- [ ] تست روی یک گوشی اندروید ارزان واقعی با نت موبایل — بارگذاری قابل قبول، لمس راحت
- [ ] همه اعداد و تاریخ‌ها فارسی/شمسی (از `lib/format.ts`)

---

# فاز ۳: کانکور + ماشین حساب چانس + آزمون رشته (هفته ۸–۹)

## مرحله ۳.۱ — ماژول `kankor` (Backend)

**جداول:**

```python
class KankorCutoff(Base):
    __tablename__ = "kankor_cutoffs"
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    department_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("departments.id"))
    year: Mapped[int]            # سال هجری شمسی مثل ۱۴۰۴
    min_score: Mapped[float]     # پایین‌ترین نمره قبولی
    capacity: Mapped[int | None] # ظرفیت پذیرش

class KankorGuide(Base):
    __tablename__ = "kankor_guides"
    id, title_fa, body_fa, category, sort_order  # مقالات راهنما
```

**منطق ماشین حساب چانس — قلب این فاز** (`kankor/service.py`):

```python
from dataclasses import dataclass

@dataclass
class ChanceResult:
    department_slug: str
    department_name: str
    chance: str          # "high" | "medium" | "low"
    last_min_score: float
    avg_min_score: float
    trend: str           # "rising" | "stable" | "falling"

class KankorService:
    def __init__(self, db):
        self.repo = KankorRepository(db)

    async def calculate_chances(self, score: float) -> list[ChanceResult]:
        """نمره تخمینی کاربر → چانس قبولی — فقط دیپارتمنت‌های فارغ‌ده"""
        results = []
        # department_type='degree': دیپارتمنت خدماتی در کانکور انتخاب نمی‌شود
        for dept in await self.repo.departments_with_cutoffs(department_type="degree"):
            cutoffs = sorted(dept.cutoffs, key=lambda c: c.year)
            if not cutoffs:
                continue
            last = cutoffs[-1].min_score
            avg = sum(c.min_score for c in cutoffs) / len(cutoffs)

            # قوانین ساده و قابل توضیح — عمداً از ML استفاده نمی‌کنیم
            if score >= last + 10:
                chance = "high"
            elif score >= last - 5:
                chance = "medium"
            else:
                chance = "low"

            trend = self._trend(cutoffs)
            results.append(ChanceResult(dept.slug, dept.name_fa, chance,
                                        last, round(avg, 1), trend))
        # مرتب‌سازی: اول چانس بالا
        order = {"high": 0, "medium": 1, "low": 2}
        return sorted(results, key=lambda r: order[r.chance])

    def _trend(self, cutoffs) -> str:
        if len(cutoffs) < 2:
            return "stable"
        diff = cutoffs[-1].min_score - cutoffs[-2].min_score
        if diff > 3: return "rising"
        if diff < -3: return "falling"
        return "stable"
```

**Endpoint:** `GET /kankor/chances?score=250` → لیست `ChanceResult`

> **نکته مهم:** کنار هر نتیجه در UI بنویسید: «این فقط تخمین بر اساس سال‌های گذشته است، تضمین قبولی نیست.» — مسئولیت اخلاقی و اعتبار پروژه.

## مرحله ۳.۲ — ماژول `quiz` (آزمون انتخاب رشته)

**جداول:** `quiz_questions`, `quiz_options` (با `trait_weights` JSON), `department_trait_profiles`

> **قانون:** پروفایل صفات فقط برای دیپارتمنت‌های **فارغ‌ده** ساخته می‌شود — آزمون هرگز دیپارتمنت خدماتی را پیشنهاد ندهد.

**منطق نمره‌دهی** (`quiz/service.py`):

```python
import math

TRAITS = ["logic", "biology", "language", "art", "social", "handson"]

def cosine_similarity(a: dict, b: dict) -> float:
    dot = sum(a.get(t, 0) * b.get(t, 0) for t in TRAITS)
    mag_a = math.sqrt(sum(a.get(t, 0) ** 2 for t in TRAITS))
    mag_b = math.sqrt(sum(b.get(t, 0) ** 2 for t in TRAITS))
    return dot / (mag_a * mag_b) if mag_a and mag_b else 0.0

class QuizService:
    async def score(self, selected_option_ids: list[uuid.UUID]) -> list[QuizMatch]:
        # ۱. جمع وزن‌های گزینه‌های انتخابی → بردار علاقه کاربر
        user_vector: dict[str, int] = {}
        for opt in await self.repo.get_options(selected_option_ids):
            for trait, w in opt.trait_weights.items():
                user_vector[trait] = user_vector.get(trait, 0) + w

        # ۲. شباهت کسینوسی با پروفایل هر رشته
        matches = []
        for profile in await self.repo.all_profiles():
            sim = cosine_similarity(user_vector, profile.trait_weights)
            matches.append(QuizMatch(profile.department_slug,
                                     round(sim * 100)))
        return sorted(matches, key=lambda m: -m.percent)[:5]
```

**محتوا:** ۳۰–۵۰ سوال (خود شما بنویسید یا با کمک AI تولید و بازبینی کنید). هر گزینه وزن ۰–۳ در شش صفت.

## مرحله ۳.۳ — صفحات وب

- `/kankor/chance`: فرم نمره → لیست کارت رشته با رنگ چانس (سبز/زرد/سرخ) + نمودار کات‌آف سال‌ها
- `/quiz`: سوال‌ها یکی‌یکی (state سمت کلاینت) → نتیجه: ۵ رشته برتر با درصد تطابق → لینک به صفحه غنی هر رشته

## ✅ تعریف تمام‌شدن فاز ۳

- [ ] کات‌آف حداقل ۳ سال اخیر برای همه رشته‌های پوهنتون هرات وارد شده (منبع: نتایج NEXA)
- [ ] نمره بزن → چانس ببین → روی رشته کلیک کن → صفحه غنی — چرخه کامل کار می‌کند
- [ ] آزمون ۳۰+ سوالی نتیجه منطقی می‌دهد (خودتان با چند پروفایل فرضی تست کنید)
- [ ] تست واحد برای `cosine_similarity` و `calculate_chances` (حداقل ۶ حالت)

---

# فاز ۴: هوش مصنوعی — RAG + چت‌بات (هفته ۱۰–۱۲)

## مرحله ۴.۱ — لایه Provider (`providers/ai/`)

```python
# providers/ai/base.py
from abc import ABC, abstractmethod

class AIProvider(ABC):
    @abstractmethod
    async def chat(self, system: str, messages: list[dict],
                   max_tokens: int = 800) -> str: ...

# providers/ai/factory.py
from app.config import settings

def get_ai_provider() -> AIProvider:
    match settings.ai_provider:
        case "gemini":     return GeminiProvider()
        case "openrouter": return OpenRouterProvider()
        case _: raise ValueError(f"AI provider ناشناخته: {settings.ai_provider}")
```

پیاده‌سازی `GeminiProvider` و `OpenRouterProvider` با `httpx` (کد نمونه در نقشه راه نسخه ۲، بخش ۹.۳).

## مرحله ۴.۲ — Embedding و جدول RAG

```python
# modules/ai/embeddings.py
from sentence_transformers import SentenceTransformer

_model: SentenceTransformer | None = None   # lazy load — فقط بار اول

def get_model() -> SentenceTransformer:
    global _model
    if _model is None:
        _model = SentenceTransformer("intfloat/multilingual-e5-small")
    return _model

def embed_query(text: str) -> list[float]:
    return get_model().encode(f"query: {text}", normalize_embeddings=True).tolist()

def embed_passage(text: str) -> list[float]:
    return get_model().encode(f"passage: {text}", normalize_embeddings=True).tolist()
```

> **دقت:** مدل e5 برای سوال پیشوند `query:` و برای متن ذخیره‌شده پیشوند `passage:` می‌خواهد — جابجا نشود، کیفیت جستجو پایین می‌آید.

```python
# modules/ai/models.py
from pgvector.sqlalchemy import Vector

class RagChunk(Base):
    __tablename__ = "rag_chunks"
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    source_type: Mapped[str]     # 'department' | 'faq' | 'kankor_guide' | 'news'
    source_id: Mapped[uuid.UUID]
    content: Mapped[str] = mapped_column(Text)
    language: Mapped[str] = mapped_column(String(5), default="fa")
    embedding = mapped_column(Vector(384))
```

Migration دستی برای index (autogenerate آن را نمی‌سازد):

```sql
CREATE EXTENSION IF NOT EXISTS vector;
CREATE INDEX ix_rag_embedding ON rag_chunks
  USING hnsw (embedding vector_cosine_ops);
```

## مرحله ۴.۳ — Indexer (ساخت دانش چت‌بات از دیتای سایت)

```python
# modules/ai/indexer.py
class RagIndexer:
    """کل محتوای سایت را قطعه‌قطعه، embed و ذخیره می‌کند"""

    CHUNK_MAX_WORDS = 400

    def __init__(self, db: AsyncSession):
        self.db = db

    async def reindex_all(self) -> int:
        """پاک‌سازی و بازسازی کامل — با دکمه ادمین صدا زده می‌شود"""
        await self.db.execute(delete(RagChunk))
        count = 0
        count += await self._index_departments()
        count += await self._index_faqs()
        count += await self._index_kankor_guides()
        await self.db.commit()
        return count

    async def _index_departments(self) -> int:
        depts = await DepartmentRepository(self.db).list_all()
        count = 0
        for d in depts:
            # هر رشته → یک متن توصیفی کامل → قطعه‌قطعه
            text = self._department_to_text(d)
            for chunk in self._split(text):
                self.db.add(RagChunk(source_type="department", source_id=d.id,
                                     content=chunk,
                                     embedding=embed_passage(chunk)))
                count += 1
        return count

    def _department_to_text(self, d) -> str:
        """Model → متن طبیعی که LLM خوب بفهمد — نوع دیپارتمنت و دیدگاه/ماموریت حتماً داخل متن"""
        if d.department_type == "service":
            type_note = ("این یک دیپارتمنت خدماتی (غیرفارغ‌ده) است: فقط خدمات آموزشی "
                         "به دیپارتمنت‌های دیگر می‌دهد و در کانکور قابل انتخاب نیست.")
        else:
            type_note = "این یک دیپارتمنت فارغ‌ده است و در کانکور قابل انتخاب است."
        return (f"دیپارتمنت {d.name_fa} در پوهنځی {d.faculty.name_fa} پوهنتون هرات. "
                f"{type_note} "
                f"دیدگاه: {d.vision_fa or ''} ماموریت: {d.mission_fa or ''} "
                f"مدت تحصیل: {d.duration_years} سال، مدرک: {d.degree_type}. "
                f"معرفی: {d.description_fa} "
                f"مضامین اصلی: {'، '.join(d.subjects)}. "
                f"مسیرهای شغلی: {'، '.join(p['title'] for p in d.career_paths)}. "
                f"بازار کار: {d.job_market_fa or ''}")

    def _split(self, text: str) -> list[str]:
        """تقسیم به قطعات حداکثر ۴۰۰ کلمه‌ای، بریدن روی مرز جمله"""
        words = text.split()
        chunks, current = [], []
        for w in words:
            current.append(w)
            if len(current) >= self.CHUNK_MAX_WORDS and w.endswith(("۔", ".", "؟", "!")):
                chunks.append(" ".join(current)); current = []
        if current:
            chunks.append(" ".join(current))
        return chunks
```

## مرحله ۴.۴ — Retriever و ChatService

```python
# modules/ai/retriever.py
class RagRetriever:
    async def retrieve(self, question: str, limit: int = 8) -> list[str]:
        q_emb = embed_query(question)
        rows = await self.db.execute(
            select(RagChunk.content)
            .order_by(RagChunk.embedding.cosine_distance(q_emb))
            .limit(limit))
        return [r[0] for r in rows]

# modules/ai/service.py
SYSTEM_PROMPT = """تو دستیار هوشمند پوهنتون هرات هستی. فقط بر اساس «اطلاعات دانشگاه»
زیر جواب بده. اگر جواب در اطلاعات نبود، صادقانه بگو نمی‌دانی و پیشنهاد کن
با دانشگاه تماس بگیرند. به زبان {language} و با لحن دوستانه و کوتاه جواب بده.

=== اطلاعات دانشگاه ===
{context}"""

class ChatService:
    def __init__(self, db: AsyncSession, redis: Redis):
        self.retriever = RagRetriever(db)
        self.provider = get_ai_provider()
        self.cache = ChatCache(redis)
        self.log_repo = ChatLogRepository(db)

    async def ask(self, session_id: str, message: str,
                  language: str = "fa") -> ChatReply:
        # ۱. کش — سوال تکراری، جواب فوری و رایگان
        cached = await self.cache.get(message, language)
        if cached:
            return ChatReply(response=cached, cached=True)

        # ۲. بازیابی دانش مرتبط
        chunks = await self.retriever.retrieve(message)
        system = SYSTEM_PROMPT.format(language=language,
                                      context="\n---\n".join(chunks))

        # ۳. پرسش از LLM
        answer = await self.provider.chat(system,
                                          [{"role": "user", "content": message}])

        # ۴. کش ۷ روزه + لاگ
        await self.cache.set(message, language, answer)
        await self.log_repo.save(session_id, message, answer)
        return ChatReply(response=answer, cached=False)
```

```python
# modules/ai/cache.py
import hashlib

class ChatCache:
    TTL = 7 * 24 * 3600

    def __init__(self, redis):
        self.redis = redis

    def _key(self, message: str, language: str) -> str:
        normalized = " ".join(message.strip().lower().split())
        return f"ai:{language}:{hashlib.sha256(normalized.encode()).hexdigest()}"

    async def get(self, message, language):
        return await self.redis.get(self._key(message, language))

    async def set(self, message, language, answer):
        await self.redis.set(self._key(message, language), answer, ex=self.TTL)
```

**Rate limit:** در `core/rate_limit.py` — با Redis شمارنده به ازای IP یا session: حداکثر ۲۰ پیام AI در روز. یک Dependency ساده FastAPI.

## مرحله ۴.۵ — صفحه چت (`web/src/app/chat/page.tsx`)

- Client Component، state لیست پیام‌ها
- `session_id`: UUID تصادفی در `localStorage` — بدون هویت واقعی
- سه دکمه پیشنهادی شروع: «کدام رشته مناسب من است؟» / «شرایط کانکور چیست؟» / «رشته کمپیوتر ساینس چطور است؟»
- نمایشگر «در حال فکر کردن…»، برچسب «پاسخ از حافظه» برای جواب کش‌شده
- خطای شبکه → پیام دوستانه + دکمه تلاش مجدد

## ✅ تعریف تمام‌شدن فاز ۴

- [ ] `POST /admin/rag/reindex` → تعداد chunk برمی‌گرداند
- [ ] سوال دری «رشته کمپیوتر ساینس چند ساله است؟» → جواب درست از داده واقعی
- [ ] سوال بی‌ربط («پایتخت فرانسه؟») → مودبانه رد می‌کند
- [ ] سوال تکراری → بار دوم `cached: true` و فوری
- [ ] پیام ۲۱ام در یک روز → خطای ۴۲۹ با پیام مناسب
- [ ] کلید API فقط در `.env` سرور — در هیچ کد کلاینتی نیست

---

# فاز ۵: پنل ادمین + نوتیفیکیشن (هفته ۱۳–۱۴)

## مرحله ۵.۱ — احراز هویت ادمین (`modules/admin_auth/`)

- جدول `admin_users` (email, hashed_password با bcrypt, role) + `refresh_tokens`
- `POST /admin/auth/login` → access token (۱۵ دقیقه) + refresh token
- `POST /admin/auth/refresh` → **Rotation**: توکن قبلی revoke، توکن جدید صادر؛ استفاده از توکن revoke شده → همه نشست‌های آن ادمین باطل
- Dependency `get_current_admin` در `core/deps.py` — روی همه روت‌های `/admin/*`

## مرحله ۵.۲ — پنل: SQLAdmin (سریع)

پکیج `sqladmin` روی همان FastAPI — برای هر Model یک کلاس `ModelView` (~۵ خط). مسئول محتوا از همین برای ورود داده استفاده می‌کند. پنل React سفارشی = فاز بعدی، فقط اگر لازم شد.

نکته: بعد از هر تغییر محتوا، دکمه/endpoint «بازسازی دانش چت‌بات» (`reindex_all`) — یا خودکار شبانه با APScheduler.

## مرحله ۵.۳ — نوتیفیکیشن (الگوی Pounce)

- جدول `academic_events` (title, event_date, remind_days_before)
- `providers/notifier/base.py` → `class NotifierProvider(ABC)` → پیاده‌سازی FCM (برای وب: Web Push)
- APScheduler: هر روز ساعت ۸ صبح:

```python
async def send_due_reminders():
    events = await repo.events_needing_reminder(today)
    for ev in events:
        await notifier.send_to_all(
            title=f"یادآوری: {ev.title_fa}",
            body=f"{ev.days_left} روز مانده — {ev.event_date_shamsi}")
```

- مهم‌ترین محتوا: تقویم کانکور (ثبت‌نام، توزیع کارت، روز امتحان، اعلام نتایج)

## ✅ تعریف تمام‌شدن فاز ۵

- [ ] مسئول محتوا (غیر برنامه‌نویس) بتواند رشته جدید + خبر + رویداد وارد کند
- [ ] لاگین ادمین امن: rotation تست شده، rate limit روی login
- [ ] یادآوری رویداد آزمایشی در زمان درست ارسال شود

---

# فاز ۶: استقرار عمومی (هفته ۱۵)

1. **سرور — گزینه الف (پیش‌فرض): سرور Ubuntu خود دانشگاه** (IP پابلیک موجود است — هزینه: صفر):
   - Docker Compose همه سرویس‌ها + Nginx + Let's Encrypt
   - پیش‌نیاز: 4GB+ RAM (چک: `free -h`) · نصب Docker: `curl -fsSL https://get.docker.com | sh`
   - پورت فوروارد فقط **80 و 443** (+ SSH ترجیحاً روی پورت غیراستاندارد)
   - امنیت: SSH فقط با کلید (پسورد خاموش) · `ufw` فعال — فقط همین سه پورت باز
   - تست از بیرون شبکه دانشگاه: `curl http://IP` با اینترنت سیم‌کارت موبایل
2. **سرور — گزینه ب (جایگزین/ارتقا):** VPS (Hetzner ~۲۰ دلار، 4GB) — اگر برق یا اینترنت سرور دانشگاه ناپایدار بود
3. **دامنه:** ساب‌دامین `guide.hu.edu.af` — یک A record در DNS دانشگاه (از طریق cPanel یا IT دانشگاه) به IP پابلیک سرور + HTTPS اجباری
4. **CI/CD**: GitHub Actions — هر push به `main`: اجرای pytest → build → deploy. تست قرمز = deploy نمی‌شود.
5. **بکاپ**: cron شبانه `pg_dump` + نگهداری ۷ نسخه + ⭐ آپلود خودکار نسخه شبانه به هاست cPanel دانشگاه (FTP) — کپی خارج از سرور، رایگان. سرور فیزیکی بمیرد، دیتا زنده است.
6. **مانیتورینگ ساده**: `/health` + UptimeRobot رایگان
7. **سئو**: ثبت در Google Search Console + ارسال sitemap
8. **Umami** برای آنالیتیکس
9. **پلن پایداری (شرایط برق افغانستان):** UPS سرور بررسی شود. اگر قطعی مکرر بود: فرانت Next.js به Vercel (رایگان) منتقل شود — Backend روی سرور دانشگاه می‌ماند؛ هنگام قطعی، صفحات کش‌شده بالا می‌مانند و فقط بخش‌های زنده (چت، چانس) موقتاً از کار می‌افتند.

## ✅ تعریف تمام‌شدن فاز ۶

- [ ] سایت روی `guide.hu.edu.af` (یا دامنه انتخابی) با HTTPS
- [ ] دسترسی از بیرون شبکه دانشگاه با اینترنت موبایل تست شده
- [ ] جستجوی «رشته کمپیوتر ساینس پوهنتون هرات» بعد از چند هفته سایت را بیاورد
- [ ] push به main → deploy خودکار
- [ ] بکاپ شبانه تایید شده + نسخه روی cPanel موجود (یک بار restore آزمایشی!)

---

# بخش پایانی: قوانین دائمی تیم

1. **هر تغییر = شاخه جدید + Pull Request + بازبینی** — هیچ push مستقیم به `main`
2. **Query دیتابیس فقط در Repository** — در بازبینی کد چک شود
3. **کلید و رمز فقط در `.env`** — commit شدن secret = تعویض فوری آن
4. **هر ماژول جدید = همان الگوی ۵ فایلی** — خلاقیت در ساختار ممنوع، خلاقیت در محتوا آزاد
5. **هر endpoint جدید = حداقل ۲ تست** (موفق + شکست)
6. **تغییر جدول فقط با Alembic migration**
7. **متن UI فقط از دیکشنری i18n** — رشته متنی hard-code در کامپوننت ممنوع
8. اگر شک کردید چیزی کجا بگذارید: **«این کد چه چیزی را می‌داند؟»** — HTTP می‌داند → router؛ قاعده تجاری می‌داند → service؛ SQL می‌داند → repository

## ترتیب گسترش آینده (بدون شکستن هیچ چیز)

| گسترش | چه چیزی تغییر می‌کند | چه چیزی تغییر نمی‌کند |
|---|---|---|
| اپ موبایل Flutter | کلاینت جدید | کل Backend |
| ربات تلگرام | کلاینت جدید | کل Backend |
| دانشگاه دوم | داده جدید + فیلتر `university_id` | معماری |
| مدل AI بهتر | یک خط `.env` | کل کد |
| Meilisearch | یک `SearchProvider` جدید | ماژول‌ها |
| PDF مقررات در چت‌بات | یک متد `_index_pdfs` در Indexer | بقیه RAG |
