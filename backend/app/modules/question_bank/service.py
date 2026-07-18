import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import NotFoundError
from .models import QuestionBank
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
        # Collection-progress breakdowns (which years/grades are covered so far)
        stats["by_year"] = await self.repo.count_grouped(QuestionBank.year)
        stats["by_grade"] = await self.repo.count_grouped(QuestionBank.grade)
        stats["verified"] = await self.repo.count_questions(verified_only=True)
        return stats

    async def generate_exam(self, subject: str | None = None, num_questions: int = 10, difficulty: str | None = None):
        """Generate a random exam from the question bank."""
        questions = await self.repo.get_random_questions(
            n=num_questions,
            subject=subject,
            difficulty=difficulty,
        )

        # Format questions for exam. Options have no persisted per-row id
        # (stored inside the question's JSON column) — use the index as the
        # id so any future scoring endpoint can map an answer back correctly.
        exam_questions = []
        for i, q in enumerate(questions):
            options = []
            for idx, opt in enumerate(q.options):
                options.append({
                    "id": str(idx),
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

    async def list_questions(
        self,
        subject: str | None = None,
        limit: int = 50,
        offset: int = 0,
        year: int | None = None,
        grade: str | None = None,
    ):
        """List questions from the bank, filterable by subject/year/grade."""
        q = select(QuestionBank).where(QuestionBank.is_active == True)
        if subject:
            q = q.where(QuestionBank.subject == subject)
        if year:
            q = q.where(QuestionBank.year == year)
        if grade:
            q = q.where(QuestionBank.grade == grade)
        q = (
            q.order_by(QuestionBank.subject, QuestionBank.difficulty)
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
        q = select(QuestionBank).where(QuestionBank.id == id)
        obj = (await self.repo.db.execute(q)).scalar_one_or_none()
        if obj is None:
            raise NotFoundError("سوال یافت نشد")
        return await self.repo.update(obj, payload.model_dump(exclude_unset=True))

    async def delete_question(self, id: uuid.UUID):
        q = select(QuestionBank).where(QuestionBank.id == id)
        obj = (await self.repo.db.execute(q)).scalar_one_or_none()
        if obj is None:
            raise NotFoundError("سوال یافت نشد")
        await self.repo.delete(obj)

    async def import_questions(self, questions: list[dict]):
        """All-or-nothing bulk import: every row is validated first; if any row
        is invalid, nothing is written and the per-row errors are returned."""
        from pydantic import ValidationError
        from .schemas import QuestionBankImportItem

        if not questions:
            return {"imported": 0, "errors": [{"row": 0, "message": "هیچ سوالی ارسال نشده"}]}

        validated = []
        errors = []
        for i, raw in enumerate(questions):
            try:
                validated.append(QuestionBankImportItem(**raw))
            except ValidationError as e:
                message = "؛ ".join(err["msg"] for err in e.errors())
                errors.append({"row": i + 1, "message": message})

        if errors:
            return {"imported": 0, "errors": errors}

        rows = []
        for item in validated:
            data = item.model_dump()
            data["id"] = uuid.uuid4()
            rows.append(data)

        count = await self.repo.bulk_create(rows)
        return {"imported": count, "errors": []}
