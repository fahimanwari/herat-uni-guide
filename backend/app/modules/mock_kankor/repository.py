import uuid
import random

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .models import MockExamSession
from app.modules.question_bank.models import QuestionBank, ExamBlueprint


class MockKankorRepository:

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_random_questions(
        self,
        n: int = 160,
        subject: str | None = None,
        year_filter: int | None = None,
    ) -> list[QuestionBank]:
        q = select(QuestionBank).where(
            QuestionBank.is_active == True,
            QuestionBank.is_verified == True,
        )
        if subject:
            q = q.where(QuestionBank.subject == subject)
        if year_filter:
            q = q.where(QuestionBank.year == year_filter)

        all_questions = list((await self.db.execute(q)).scalars())

        if len(all_questions) <= n:
            return all_questions
        return random.sample(all_questions, n)

    async def get_questions_by_ids(self, ids: list[str]) -> list[QuestionBank]:
        q = select(QuestionBank).where(QuestionBank.id.in_(ids))
        return list((await self.db.execute(q)).scalars())

    async def create_session(self, data: dict) -> MockExamSession:
        obj = MockExamSession(**data)
        self.db.add(obj)
        await self.db.commit()
        await self.db.refresh(obj)
        return obj

    async def update_session(self, obj: MockExamSession, data: dict) -> MockExamSession:
        for key, value in data.items():
            setattr(obj, key, value)
        await self.db.commit()
        await self.db.refresh(obj)
        return obj

    async def get_session(self, session_id: str) -> MockExamSession | None:
        q = select(MockExamSession).where(MockExamSession.session_id == session_id)
        return (await self.db.execute(q)).scalar_one_or_none()

    async def get_sessions(self, session_id: str) -> list[MockExamSession]:
        q = (
            select(MockExamSession)
            .where(MockExamSession.session_id == session_id)
            .order_by(MockExamSession.created_at.desc())
        )
        return list((await self.db.execute(q)).scalars())

    # --- Exam blueprints ---

    async def list_active_blueprints(self) -> list[ExamBlueprint]:
        q = select(ExamBlueprint).where(ExamBlueprint.is_active == True)
        return list((await self.db.execute(q)).scalars())

    async def get_blueprint(self, id: uuid.UUID) -> ExamBlueprint | None:
        return await self.db.get(ExamBlueprint, id)

    async def create_blueprint(self, data: dict) -> ExamBlueprint:
        obj = ExamBlueprint(**data)
        self.db.add(obj)
        await self.db.commit()
        await self.db.refresh(obj)
        return obj

    async def update_blueprint(self, obj: ExamBlueprint, data: dict) -> ExamBlueprint:
        for key, value in data.items():
            setattr(obj, key, value)
        await self.db.commit()
        await self.db.refresh(obj)
        return obj

    async def delete_blueprint(self, obj: ExamBlueprint) -> None:
        await self.db.delete(obj)
        await self.db.commit()
