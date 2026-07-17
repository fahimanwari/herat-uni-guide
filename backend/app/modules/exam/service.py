import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import NotFoundError
from .repository import ExamRepository
from .schemas import SubmitExamRequest, ExamResultResponse


class ExamService:

    def __init__(self, db: AsyncSession):
        self.repo = ExamRepository(db)

    async def list_exams(self, category: str | None = None):
        return await self.repo.list_exams(category)

    async def get_exam(self, id: uuid.UUID):
        exam = await self.repo.get_exam(id)
        if exam is None:
            raise NotFoundError("امتحان یافت نشد")
        return exam

    async def submit_exam(self, exam_id: uuid.UUID, payload: SubmitExamRequest):
        exam = await self.repo.get_exam_with_correct_answers(exam_id)
        if exam is None:
            raise NotFoundError("امتحان یافت نشد")

        # Calculate score
        correct = 0
        total_points = 0
        earned_points = 0

        for question in exam.questions:
            total_points += question.points
            selected_option_id = payload.answers.get(str(question.id))
            if selected_option_id:
                for option in question.options:
                    if str(option.id) == selected_option_id and option.is_correct:
                        correct += 1
                        earned_points += question.points
                        break

        score = round((earned_points / total_points * 100) if total_points > 0 else 0, 1)

        # Save result
        result = await self.repo.create_result({
            "exam_id": exam_id,
            "session_id": payload.session_id,
            "score": score,
            "total_points": total_points,
            "correct_answers": correct,
            "total_answers": len(exam.questions),
            "answers": payload.answers,
            "time_taken_seconds": payload.time_taken_seconds,
        })

        return {
            "result_id": str(result.id),
            "score": score,
            "correct_answers": correct,
            "total_answers": len(exam.questions),
            "total_points": total_points,
            "earned_points": earned_points,
            "percentage": score,
            "time_taken_seconds": payload.time_taken_seconds,
        }

    async def get_results(self, session_id: str):
        return await self.repo.get_results(session_id)

    async def get_stats(self, exam_id: uuid.UUID):
        return await self.repo.get_stats(exam_id)
