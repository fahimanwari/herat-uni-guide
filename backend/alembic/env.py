import asyncio
from logging.config import fileConfig

from sqlalchemy import pool
from sqlalchemy.ext.asyncio import async_engine_from_config

from alembic import context

from app.config import settings
from app.database import Base

# Import all models so Alembic can detect them
from app.modules.universities.models import University
from app.modules.faculties.models import Faculty
from app.modules.departments.models import Department, StudentProject, AlumniStory, CareerRoadmap, DepartmentVideo
from app.modules.news.models import News
from app.modules.faqs.models import Faq
from app.modules.kankor.models import KankorCutoff, KankorGuide
from app.modules.quiz.models import QuizQuestion, QuizOption, DepartmentTraitProfile
from app.modules.ai.models import RagChunk, AiChatLog
from app.modules.admin_auth.models import AdminUser, RefreshToken
from app.modules.notifications.models import AcademicEvent
from app.modules.exam.models import Exam, ExamQuestion, ExamOption, ExamResult
from app.modules.users.models import User
from app.modules.question_bank.models import QuestionBank, ExamBlueprint
from app.modules.mock_kankor.models import MockExamSession
from app.modules.achievements.models import UserAchievement

config = context.config
config.set_main_option("sqlalchemy.url", settings.database_url)

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata


def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection):
    context.configure(connection=connection, target_metadata=target_metadata)
    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)
    await connectable.dispose()


def run_migrations_online() -> None:
    asyncio.run(run_async_migrations())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
