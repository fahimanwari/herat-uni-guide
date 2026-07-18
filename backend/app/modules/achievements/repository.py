import uuid
from datetime import datetime, timedelta

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from .models import UserAchievement


BADGES = {
    "first_exam": {"name": "اولین قدم", "emoji": "🎯", "condition": "اولین آزمون"},
    "five_exams": {"name": "تمرین‌کننده", "emoji": "📚", "condition": "۵ آزمون"},
    "ten_exams": {"name": "استاد تمرین", "emoji": "🏆", "condition": "۱۰ آزمون"},
    "score_200": {"name": "نمره بالای ۲۰۰", "emoji": "⭐", "condition": "نمره ≥ ۲۰۰ از ۳۶۰"},
    "score_280": {"name": "نمره بالای ۲۸۰", "emoji": "🌟", "condition": "نمره ≥ ۲۸۰ از ۳۶۰"},
    "score_320": {"name": "نخبه", "emoji": "💎", "condition": "نمره ≥ ۳۲۰ از ۳۶۰"},
    "streak_3": {"name": "۳ روز پشت‌سرهم", "emoji": "🔥", "condition": "۳ روز متوالی آزمون"},
    "streak_7": {"name": "۷ روز پشت‌سرهم", "emoji": "💪", "condition": "۷ روز متوالی آزمون"},
    "math_master": {"name": "استاد ریاضی", "emoji": "🔢", "condition": "نمره ریاضی ≥ ۸۰٪"},
    "science_master": {"name": "استاد علوم", "emoji": "🧬", "condition": "نمره بیولوژی ≥ ۸۰٪"},
}


class AchievementRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_achievements(self, session_id: str) -> list[UserAchievement]:
        q = (
            select(UserAchievement)
            .where(UserAchievement.session_id == session_id)
            .order_by(UserAchievement.earned_at.desc())
        )
        return list((await self.db.execute(q)).scalars())

    async def has_badge(self, session_id: str, badge_key: str) -> bool:
        q = select(UserAchievement).where(
            UserAchievement.session_id == session_id,
            UserAchievement.badge_key == badge_key,
        )
        return (await self.db.execute(q)).scalar_one_or_none() is not None

    async def award(self, session_id: str, badge_key: str) -> UserAchievement:
        obj = UserAchievement(session_id=session_id, badge_key=badge_key)
        self.db.add(obj)
        await self.db.commit()
        await self.db.refresh(obj)
        return obj

    async def get_leaderboard(self, days: int = 7) -> list[dict]:
        cutoff = datetime.utcnow() - timedelta(days=days)
        from app.modules.mock_kankor.models import MockExamSession
        q = (
            select(
                MockExamSession.session_id,
                func.max(MockExamSession.score).label("best_score"),
            )
            .where(
                MockExamSession.completed_at.isnot(None),
                MockExamSession.created_at >= cutoff,
            )
            .group_by(MockExamSession.session_id)
            .order_by(func.max(MockExamSession.score).desc())
            .limit(10)
        )
        results = (await self.db.execute(q)).all()
        return [
            {"rank": i + 1, "score": r.best_score or 0, "display_name": f"شاگرد {i + 1}"}
            for i, r in enumerate(results)
        ]
