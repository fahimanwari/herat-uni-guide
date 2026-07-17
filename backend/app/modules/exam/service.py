import uuid
from datetime import datetime

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import NotFoundError
from .repository import ExamRepository
from .schemas import ExamResultResponse


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

    async def submit_exam(self, exam_id: uuid.UUID, payload):
        exam = await self.repo.get_exam_with_correct_answers(exam_id)
        if exam is None:
            raise NotFoundError("امتحان یافت نشد")

        # Build correct answers map
        correct_map = {}
        for question in exam.questions:
            for option in question.options:
                if option.is_correct:
                    correct_map[str(question.id)] = str(option.id)
                    break

        # Calculate scores
        correct = 0
        wrong = 0
        empty = 0
        total_points = 0
        earned_points = 0
        subject_scores = {}
        detailed_answers = {}

        for question in exam.questions:
            total_points += question.points
            selected_option_id = payload.answers.get(str(question.id))

            if not selected_option_id:
                empty += 1
                detailed_answers[str(question.id)] = {
                    "selected": None,
                    "correct": correct_map.get(str(question.id)),
                    "is_correct": False,
                }
                continue

            is_correct = selected_option_id == correct_map.get(str(question.id))

            if is_correct:
                correct += 1
                earned_points += question.points
            else:
                wrong += 1

            # Track subject scores
            subject = question.subject or "general"
            if subject not in subject_scores:
                subject_scores[subject] = {"correct": 0, "total": 0}
            subject_scores[subject]["total"] += 1
            if is_correct:
                subject_scores[subject]["correct"] += 1

            detailed_answers[str(question.id)] = {
                "selected": selected_option_id,
                "correct": correct_map.get(str(question.id)),
                "is_correct": is_correct,
            }

        # Calculate percentage
        score = round((earned_points / total_points * 100) if total_points > 0 else 0, 1)

        # Calculate subject percentages
        for subj, data in subject_scores.items():
            data["percentage"] = round((data["correct"] / data["total"] * 100) if data["total"] > 0 else 0, 1)

        # Compare to average
        avg_score = await self._get_average_score(exam_id)
        compared_to_avg = round(score - avg_score, 1) if avg_score > 0 else None

        # Determine if passed
        passed = score >= exam.passing_score

        # Parse started_at
        started_at = None
        if payload.started_at:
            try:
                started_at = datetime.fromisoformat(payload.started_at.replace("Z", "+00:00"))
            except:
                pass

        # Save result
        result = await self.repo.create_result({
            "exam_id": exam_id,
            "user_id": uuid.UUID(payload.user_id) if payload.user_id else None,
            "session_id": payload.session_id,
            "score": score,
            "raw_score": earned_points,
            "total_points": total_points,
            "correct_answers": correct,
            "wrong_answers": wrong,
            "empty_answers": empty,
            "total_answers": len(exam.questions),
            "subject_scores": subject_scores,
            "answers": detailed_answers,
            "time_taken_seconds": payload.time_taken_seconds,
            "started_at": started_at,
            "completed_at": datetime.utcnow(),
            "exam_year": exam.year,
            "compared_to_avg": compared_to_avg,
        })

        return {
            "result_id": str(result.id),
            "score": score,
            "raw_score": earned_points,
            "correct_answers": correct,
            "wrong_answers": wrong,
            "empty_answers": empty,
            "total_answers": len(exam.questions),
            "total_points": total_points,
            "subject_scores": subject_scores,
            "percentage": score,
            "passed": passed,
            "passing_score": exam.passing_score,
            "compared_to_avg": compared_to_avg,
            "time_taken_seconds": payload.time_taken_seconds,
        }

    async def get_results(self, session_id: str):
        return await self.repo.get_results(session_id)

    async def get_stats(self, exam_id: uuid.UUID):
        return await self.repo.get_stats(exam_id)

    async def get_user_stats(self, session_id: str):
        """Get comprehensive stats for a user."""
        results = await self.repo.get_results(session_id)
        if not results:
            return {
                "total_exams": 0,
                "average_score": 0,
                "best_score": 0,
                "worst_score": 0,
                "total_time_minutes": 0,
                "subject_averages": {},
                "improvement_trend": "stable",
                "rank_estimate": "N/A",
            }

        scores = [r.score for r in results]
        times = [r.time_taken_seconds or 0 for r in results]

        # Subject averages
        all_subject_scores = {}
        for r in results:
            for subj, data in r.subject_scores.items():
                if subj not in all_subject_scores:
                    all_subject_scores[subj] = []
                all_subject_scores[subj].append(data.get("percentage", 0))

        subject_averages = {
            subj: round(sum(vals) / len(vals), 1)
            for subj, vals in all_subject_scores.items()
        }

        # Improvement trend
        if len(scores) >= 3:
            recent = scores[-3:]
            if recent[-1] > recent[0]:
                trend = "improving"
            elif recent[-1] < recent[0]:
                trend = "declining"
            else:
                trend = "stable"
        else:
            trend = "stable"

        # Rank estimate (rough)
        avg = sum(scores) / len(scores)
        if avg >= 90:
            rank = "top 10%"
        elif avg >= 75:
            rank = "top 25%"
        elif avg >= 60:
            rank = "top 50%"
        else:
            rank = "below average"

        return {
            "total_exams": len(results),
            "average_score": round(avg, 1),
            "best_score": max(scores),
            "worst_score": min(scores),
            "total_time_minutes": round(sum(times) / 60, 1),
            "subject_averages": subject_averages,
            "improvement_trend": trend,
            "rank_estimate": rank,
        }

    async def get_year_comparison(self, exam_id: uuid.UUID):
        """Compare scores across different years."""
        exam = await self.repo.get_exam(exam_id)
        if not exam:
            raise NotFoundError("امتحان یافت نشد")

        # Get all results for this exam
        results = await self.repo.get_results_for_exam(exam_id)

        # Group by year
        year_data = {}
        for r in results:
            year = r.exam_year or 0
            if year not in year_data:
                year_data[year] = {"scores": [], "count": 0}
            year_data[year]["scores"].append(r.score)
            year_data[year]["count"] += 1

        # Calculate averages per year
        comparison = []
        for year, data in sorted(year_data.items()):
            avg = sum(data["scores"]) / len(data["scores"]) if data["scores"] else 0
            comparison.append({
                "year": year,
                "average_score": round(avg, 1),
                "attempts": data["count"],
                "min_score": min(data["scores"]) if data["scores"] else 0,
                "max_score": max(data["scores"]) if data["scores"] else 0,
            })

        return {
            "exam_title": exam.title_fa,
            "exam_year": exam.year,
            "comparison": comparison,
            "note": "نمرات هر سال بسته به سطح دشواری امتحان متفاوت است",
        }

    async def _get_average_score(self, exam_id: uuid.UUID) -> float:
        from .models import ExamResult
        q = select(func.avg(ExamResult.score)).where(ExamResult.exam_id == exam_id)
        result = (await self.repo.db.execute(q)).scalar()
        return result or 0
