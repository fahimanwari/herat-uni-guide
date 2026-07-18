import uuid
from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import NotFoundError
from .repository import MockKankorRepository
from app.modules.question_bank.models import QuestionBank


class MockKankorService:

    def __init__(self, db: AsyncSession):
        self.repo = MockKankorRepository(db)

    async def start_exam(
        self,
        session_id: str,
        subject: str | None = None,
        num_questions: int = 160,
        year_filter: int | None = None,
        blueprint_id: str | None = None,
    ):
        total_minutes = 160
        if blueprint_id:
            blueprint = await self.repo.get_blueprint(uuid.UUID(blueprint_id))
            if blueprint is None or not blueprint.is_active:
                raise NotFoundError("الگوی امتحان یافت نشد")
            # Respect the blueprint's per-subject section counts instead of
            # sampling flat across all subjects (which skews subject balance).
            questions = []
            for section in blueprint.sections:
                questions.extend(await self.repo.get_random_questions(
                    n=section["count"], subject=section["subject"], year_filter=year_filter,
                ))
            total_minutes = blueprint.total_minutes
        else:
            questions = await self.repo.get_random_questions(n=num_questions, subject=subject, year_filter=year_filter)

        if not questions:
            raise NotFoundError("سوالی یافت نشد — بانک سوالات خالی است")

        # Create session
        question_ids = [str(q.id) for q in questions]
        await self.repo.create_session({
            "id": uuid.uuid4(),
            "session_id": session_id,
            "blueprint_id": uuid.UUID(blueprint_id) if blueprint_id else None,
            "questions": question_ids,
            "answers": {},
            "started_at": datetime.utcnow(),
            "score": None,
            "subject_scores": {},
        })

        # Format questions for response. Options have no persisted per-row id
        # (they live inside the question's JSON column) — the option's index
        # IS its id, and submit_exam/review_exam key answers by that same
        # index, so it must NOT be replaced with a random uuid here.
        formatted = []
        for i, q in enumerate(questions):
            options = [{"id": str(idx), "text": opt["text"]} for idx, opt in enumerate(q.options)]
            formatted.append({
                "id": str(q.id),
                "question_fa": q.question_fa,
                "options": options,
                "subject": q.subject,
                "sort_order": i,
            })

        return {
            "session_id": session_id,
            "questions": formatted,
            "total_questions": len(formatted),
            "total_minutes": total_minutes,
        }

    async def submit_exam(self, session_id: str, answers: dict, time_taken_seconds: int | None = None):
        session = await self.repo.get_session(session_id)
        if session is None:
            raise NotFoundError("جلسه امتحان یافت نشد")

        # Get questions with correct answers
        questions = await self.repo.get_questions_by_ids(session.questions)

        # Calculate scores
        correct = 0
        wrong = 0
        empty = 0
        subject_scores = {}

        for q in questions:
            qid = str(q.id)
            selected = answers.get(qid)

            if not selected:
                empty += 1
                continue

            # Check if correct
            is_correct = False
            for i, opt in enumerate(q.options):
                if str(i) == selected and opt.get("is_correct"):
                    is_correct = True
                    break

            if is_correct:
                correct += 1
            else:
                wrong += 1

            # Track subject scores
            subj = q.subject
            if subj not in subject_scores:
                subject_scores[subj] = {"correct": 0, "total": 0}
            subject_scores[subj]["total"] += 1
            if is_correct:
                subject_scores[subj]["correct"] += 1

        total = correct + wrong + empty
        score = round((correct / total * 100) if total > 0 else 0, 1)
        # نمره به مقیاس کانکور واقعی (نمره کل ۳۶۰) — تخمینی، چون وزن رسمی هر
        # سوال منتشر نمی‌شود؛ فرض: همه سوالات هم‌وزن.
        score_360 = round((correct / total * 360) if total > 0 else 0, 1)

        # Calculate subject percentages
        for subj, data in subject_scores.items():
            data["percentage"] = round((data["correct"] / data["total"] * 100) if data["total"] > 0 else 0, 1)

        # Update session
        await self.repo.update_session(session, {
            "answers": answers,
            "completed_at": datetime.utcnow(),
            "score": score,
            "subject_scores": subject_scores,
            "time_taken_seconds": time_taken_seconds,
        })

        return {
            "session_id": session_id,
            "score": score,
            "score_360": score_360,
            "correct_answers": correct,
            "wrong_answers": wrong,
            "empty_answers": empty,
            "total_answers": total,
            "subject_scores": subject_scores,
            "passed": score >= 50,
            "time_taken_seconds": time_taken_seconds,
        }

    async def review_exam(self, session_id: str):
        session = await self.repo.get_session(session_id)
        if session is None:
            raise NotFoundError("جلسه امتحان یافت نشد")

        questions = await self.repo.get_questions_by_ids(session.questions)
        review = []

        for q in questions:
            qid = str(q.id)
            user_answer = session.answers.get(qid)

            # Find correct answer
            correct_text = ""
            is_correct = False
            for i, opt in enumerate(q.options):
                if opt.get("is_correct"):
                    correct_text = opt["text"]
                if str(i) == user_answer and opt.get("is_correct"):
                    is_correct = True

            review.append({
                "question_fa": q.question_fa,
                "subject": q.subject,
                "user_answer": user_answer,
                "correct_answer": correct_text,
                "is_correct": is_correct,
                "explanation": q.explanation_fa,
                "options": q.options,
            })

        return {
            "session_id": session_id,
            "questions": review,
            "score": session.score,
            "subject_scores": session.subject_scores,
        }

    async def get_history(self, session_id: str):
        return await self.repo.get_sessions(session_id)

    # --- Exam blueprints ---

    async def list_blueprints(self):
        return await self.repo.list_active_blueprints()

    async def create_blueprint(self, payload):
        data = payload.model_dump()
        data["id"] = uuid.uuid4()
        return await self.repo.create_blueprint(data)

    async def update_blueprint(self, id: uuid.UUID, payload):
        obj = await self.repo.get_blueprint(id)
        if obj is None:
            raise NotFoundError("الگوی امتحان یافت نشد")
        return await self.repo.update_blueprint(obj, payload.model_dump(exclude_unset=True))

    async def delete_blueprint(self, id: uuid.UUID):
        obj = await self.repo.get_blueprint(id)
        if obj is None:
            raise NotFoundError("الگوی امتحان یافت نشد")
        await self.repo.delete_blueprint(obj)
