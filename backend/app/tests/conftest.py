import pytest_asyncio
from httpx import AsyncClient, ASGITransport

from app.main import app
from app.core.deps import get_db
from app.database import engine, SessionLocal

# Import all models
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


async def override_get_db():
    async with SessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()


app.dependency_overrides[get_db] = override_get_db


@pytest_asyncio.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        yield c
