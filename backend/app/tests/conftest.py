import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.pool import NullPool

from app.config import settings
from app.main import app
from app.core.deps import get_db
from app.core.rate_limit import rate_limiter

# Import all models so metadata is complete
from app.modules.universities.models import University
from app.modules.faculties.models import Faculty
from app.modules.departments.models import Department, StudentProject, AlumniStory, CareerRoadmap
from app.modules.kankor.models import KankorCutoff, KankorGuide
from app.modules.quiz.models import QuizQuestion, QuizOption, DepartmentTraitProfile
from app.modules.ai.models import RagChunk, AiChatLog
from app.modules.admin_auth.models import AdminUser, RefreshToken
from app.modules.notifications.models import AcademicEvent
from app.modules.news.models import News
from app.modules.faqs.models import Faq


@pytest_asyncio.fixture
async def client():
    # engine مخصوص هر تست با NullPool — وگرنه کانکشن‌های pool به event loop
    # تستِ قبلی چسبیده‌اند و InterfaceError می‌گیریم
    engine = create_async_engine(settings.database_url, poolclass=NullPool)
    TestSession = async_sessionmaker(engine, expire_on_commit=False)

    async def override_get_db():
        async with TestSession() as session:
            yield session

    app.dependency_overrides[get_db] = override_get_db
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        yield c
    app.dependency_overrides.clear()
    await engine.dispose()

    # rate_limiter is a module-level singleton that lazily caches a Redis
    # connection bound to whichever event loop first used it — same class of
    # bug as the DB engine above. Reset it so the next test's loop gets a
    # fresh connection instead of "Future attached to a different loop".
    if rate_limiter.redis is not None:
        await rate_limiter.redis.aclose()
        rate_limiter.redis = None


_cached_admin_token: str | None = None


@pytest_asyncio.fixture
async def admin_token(client):
    # /admin/auth/login is rate-limited (5/min) — cache across tests instead
    # of every test that needs an admin token triggering its own login.
    global _cached_admin_token
    if _cached_admin_token is None:
        res = await client.post("/api/v1/admin/auth/login", json={
            "email": "admin@herat-uni.edu.af",
            "password": "admin123",
        })
        _cached_admin_token = res.json()["access_token"]
    return _cached_admin_token


@pytest_asyncio.fixture
async def auth_headers(admin_token):
    return {"Authorization": f"Bearer {admin_token}"}
