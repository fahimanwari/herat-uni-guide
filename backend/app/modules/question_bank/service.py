import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from .repository import QuestionBankRepository


class QuestionBankService:

    def __init__(self, db: AsyncSession):
        self.repo = QuestionBankRepository(db)

    async def get_stats(self):
        """Get statistics about the question bank."""
        subjects = await self.repo.get_all_subjects()
        stats = {}
        total = 0
        for subject in subjects:
            count = await self.repo.count_questions(subject=subject)
            stats[subject] = count
            total += count
        stats["total"] = total
        return stats

    async def generate_exam(self, subject: str | None = None, num_questions: int = 10, difficulty: str | None = None):
        """Generate a random exam from the question bank."""
        questions = await self.repo.get_random_questions(
            n=num_questions,
            subject=subject,
            difficulty=difficulty,
        )

        # Format questions for exam
        exam_questions = []
        for i, q in enumerate(questions):
            options = []
            for opt in q.options:
                options.append({
                    "id": str(uuid.uuid4()),
                    "text": opt["text"],
                })
            exam_questions.append({
                "id": str(q.id),
                "question_fa": q.question_fa,
                "options": options,
                "sort_order": i,
                "points": 1,
                "subject": q.subject,
                "difficulty": q.difficulty,
            })

        return {
            "questions": exam_questions,
            "total_questions": len(exam_questions),
            "subject": subject or "mixed",
            "difficulty": difficulty or "mixed",
        }

    async def list_questions(self, subject: str | None = None, limit: int = 50, offset: int = 0):
        """List questions from the bank."""
        if subject:
            return await self.repo.get_by_subject(subject)
        # Get all with limit/offset
        from sqlalchemy import select
        from .models import QuestionBank
        q = (
            select(QuestionBank)
            .where(QuestionBank.is_active == True)
            .order_by(QuestionBank.subject, QuestionBank.difficulty)
            .limit(limit)
            .offset(offset)
        )
        result = await self.repo.db.execute(q)
        return list(result.scalars())

    # --- CRUD ---

    async def create_question(self, payload):
        data = payload.model_dump()
        data["id"] = uuid.uuid4()
        return await self.repo.create(data)

    async def update_question(self, id: uuid.UUID, payload):
        from .models import QuestionBank
        q = select(QuestionBank).where(QuestionBank.id == id)
        obj = (await self.repo.db.execute(q)).scalar_one_or_none()
        if obj is None:
            from app.core.exceptions import NotFoundError
            raise NotFoundError("سوال یافت نشد")
        return await self.repo.update(obj, payload.model_dump(exclude_unset=True))

    async def delete_question(self, id: uuid.UUID):
        from .models import QuestionBank
        q = select(QuestionBank).where(QuestionBank.id == id)
        obj = (await self.repo.db.execute(q)).scalar_one_or_none()
        if obj is None:
            from app.core.exceptions import NotFoundError
            raise NotFoundError("سوال یافت نشد")
        await self.repo.delete(obj)

    async def import_questions(self, questions: list):
        count = 0
        for q in questions:
            data = q.model_dump()
            data["id"] = uuid.uuid4()
            await self.repo.create(data)
            count += 1
        return {"imported": count}
