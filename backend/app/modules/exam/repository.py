import uuid

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from .models import Exam, ExamQuestion, ExamOption, ExamResult


class ExamRepository:

    def __init__(self, db: AsyncSession):
        self.db = db

    async def list_exams(self, category: str | None = None) -> list[Exam]:
        q = select(Exam).where(Exam.is_active == True)
        if category:
            q = q.where(Exam.category == category)
        q = q.order_by(Exam.created_at.desc())
        return list((await self.db.execute(q)).scalars())

    async def get_exam(self, id: uuid.UUID) -> Exam | None:
        q = (
            select(Exam)
            .options(
                selectinload(Exam.questions).selectinload(ExamQuestion.options),
                selectinload(Exam.results),
            )
            .where(Exam.id == id)
        )
        return (await self.db.execute(q)).scalar_one_or_none()

    async def get_exam_with_correct_answers(self, id: uuid.UUID) -> Exam | None:
        q = (
            select(Exam)
            .options(
                selectinload(Exam.questions).selectinload(ExamQuestion.options)
            )
            .where(Exam.id == id)
        )
        return (await self.db.execute(q)).scalar_one_or_none()

    async def create_result(self, data: dict) -> ExamResult:
        obj = ExamResult(**data)
        self.db.add(obj)
        await self.db.commit()
        await self.db.refresh(obj)
        return obj

    async def get_results(self, session_id: str) -> list[ExamResult]:
        q = (
            select(ExamResult)
            .where(ExamResult.session_id == session_id)
            .order_by(ExamResult.created_at.desc())
        )
        return list((await self.db.execute(q)).scalars())

    async def get_stats(self, exam_id: uuid.UUID) -> dict:
        q = select(
            func.count(ExamResult.id).label("total_attempts"),
            func.avg(ExamResult.score).label("avg_score"),
            func.max(ExamResult.score).label("max_score"),
        ).where(ExamResult.exam_id == exam_id)
        result = (await self.db.execute(q)).one()
        return {
            "total_attempts": result.total_attempts or 0,
            "avg_score": round(result.avg_score or 0, 1),
            "max_score": result.max_score or 0,
        }

    async def get_results_for_exam(self, exam_id: uuid.UUID) -> list[ExamResult]:
        q = (
            select(ExamResult)
            .where(ExamResult.exam_id == exam_id)
            .order_by(ExamResult.created_at.desc())
        )
        return list((await self.db.execute(q)).scalars())

    # --- CRUD ---

    async def create(self, data: dict) -> Exam:
        obj = Exam(**data)
        self.db.add(obj)
        await self.db.commit()
        await self.db.refresh(obj)
        return obj

    async def update(self, obj: Exam, data: dict) -> Exam:
        for key, value in data.items():
            setattr(obj, key, value)
        await self.db.commit()
        await self.db.refresh(obj)
        return obj

    async def delete(self, obj: Exam) -> None:
        await self.db.delete(obj)
        await self.db.commit()

    # --- Question CRUD ---

    async def create_question(self, exam_id: uuid.UUID, data: dict) -> ExamQuestion:
        obj = ExamQuestion(exam_id=exam_id, **data)
        self.db.add(obj)
        await self.db.commit()
        await self.db.refresh(obj)
        return obj

    async def get_question(self, question_id: uuid.UUID) -> ExamQuestion | None:
        q = (
            select(ExamQuestion)
            .options(selectinload(ExamQuestion.options))
            .where(ExamQuestion.id == question_id)
        )
        return (await self.db.execute(q)).scalar_one_or_none()

    async def delete_question(self, obj: ExamQuestion) -> None:
        await self.db.delete(obj)
        await self.db.commit()

    async def create_option(self, question_id: uuid.UUID, data: dict) -> ExamOption:
        obj = ExamOption(question_id=question_id, **data)
        self.db.add(obj)
        await self.db.commit()
        await self.db.refresh(obj)
        return obj

    async def delete_option(self, obj: ExamOption) -> None:
        await self.db.delete(obj)
        await self.db.commit()
