import uuid
import random

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from .models import QuestionBank


class QuestionBankRepository:

    def __init__(self, db: AsyncSession):
        self.db = db

    async def count_questions(self, subject: str | None = None, difficulty: str | None = None) -> int:
        q = select(func.count(QuestionBank.id)).where(QuestionBank.is_active == True)
        if subject:
            q = q.where(QuestionBank.subject == subject)
        if difficulty:
            q = q.where(QuestionBank.difficulty == difficulty)
        result = (await self.db.execute(q)).scalar()
        return result or 0

    async def get_random_questions(
        self,
        n: int,
        subject: str | None = None,
        difficulty: str | None = None,
    ) -> list[QuestionBank]:
        """Get n random questions from the bank."""
        q = select(QuestionBank).where(QuestionBank.is_active == True)
        if subject:
            q = q.where(QuestionBank.subject == subject)
        if difficulty:
            q = q.where(QuestionBank.difficulty == difficulty)

        all_questions = list((await self.db.execute(q)).scalars())

        # Random selection without replacement
        if len(all_questions) <= n:
            return all_questions
        return random.sample(all_questions, n)

    async def get_by_subject(self, subject: str) -> list[QuestionBank]:
        q = (
            select(QuestionBank)
            .where(QuestionBank.subject == subject, QuestionBank.is_active == True)
            .order_by(QuestionBank.difficulty)
        )
        return list((await self.db.execute(q)).scalars())

    async def get_all_subjects(self) -> list[str]:
        q = select(QuestionBank.subject).distinct().where(QuestionBank.is_active == True)
        result = await self.db.execute(q)
        return [r[0] for r in result.all()]

    async def create(self, data: dict) -> QuestionBank:
        obj = QuestionBank(**data)
        self.db.add(obj)
        await self.db.commit()
        await self.db.refresh(obj)
        return obj

    async def bulk_create(self, items: list[dict]) -> int:
        count = 0
        for item in items:
            self.db.add(QuestionBank(**item))
            count += 1
        await self.db.commit()
        return count
