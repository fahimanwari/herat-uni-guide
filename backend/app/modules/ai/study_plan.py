from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.mock_kankor.models import MockExamSession


class StudyPlanService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def generate(self, session_id: str) -> dict:
        # Get recent exam sessions
        q = (
            select(MockExamSession)
            .where(
                MockExamSession.session_id == session_id,
                MockExamSession.completed_at.isnot(None),
            )
            .order_by(MockExamSession.created_at.desc())
            .limit(5)
        )
        sessions = list((await self.db.execute(q)).scalars())

        if not sessions:
            return {
                "plan": "هنوز آزمونی نداده‌اید. ابتدا یک کانکور آزمایشی بدهید تا نقاط ضعف شما را بشناسم.",
                "weak_subjects": [],
                "days_until_kankor": None,
            }

        # Analyze subject scores
        all_subjects: dict[str, list[float]] = {}
        for s in sessions:
            if s.subject_scores:
                for subj, data in s.subject_scores.items():
                    if subj not in all_subjects:
                        all_subjects[subj] = []
                    all_subjects[subj].append(data.get("percentage", 0))

        avg_scores = {subj: sum(vals) / len(vals) for subj, vals in all_subjects.items()}
        weak_subjects = sorted(avg_scores.items(), key=lambda x: x[1])[:3]

        # Build prompt
        weak_text = "، ".join(f"{subj} ({score:.0f}%)" for subj, score in weak_subjects)
        prompt = f"""
تو مشاور تحصیلی کانکور هستی. نقاط ضعف شاگرد: {weak_text}.
یک برنامه مطالعه هفتگی واقع‌بینانه به دری بساز:
- هر روز حداکثر ۳ ساعت
- مضامین ضعیف‌تر وقت بیشتر
- هر هفته یک آزمون آزمایشی کامل
- خروجی: جدول روز-به-روز ساده
- به مدت ۴ هفته
"""

        # Call AI
        try:
            from app.providers.ai.factory import get_ai_provider
            provider = get_ai_provider()
            plan_text = await provider.chat(prompt, [], max_tokens=800)
        except Exception:
            plan_text = self._fallback_plan(weak_subjects)

        return {
            "plan": plan_text,
            "weak_subjects": [{"subject": s, "avg_score": round(v, 1)} for s, v in weak_subjects],
            "avg_scores": {s: round(v, 1) for s, v in avg_scores.items()},
            "total_exams": len(sessions),
            "best_score": max(s.score or 0 for s in sessions),
        }

    def _fallback_plan(self, weak_subjects) -> str:
        lines = ["برنامه مطالعه ۴ هفته‌ای:", ""]
        for i in range(1, 5):
            lines.append(f"هفته {i}:")
            for subj, score in weak_subjects:
                hours = 3 if score < 50 else 2
                lines.append(f"  - {subj}: {hours} ساعت ({'تمرین' if score < 50 else 'مرور'})")
            lines.append(f"  - آزمون آزمایشی کامل")
            lines.append("")
        return "\n".join(lines)
