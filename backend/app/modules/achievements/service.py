import uuid
from datetime import datetime, timedelta

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from .repository import AchievementRepository, BADGES
from .schemas import AchievementSchema


class AchievementService:
    def __init__(self, db: AsyncSession):
        self.repo = AchievementRepository(db)

    async def check_and_award(self, session_id: str) -> list[str]:
        """Check all badge conditions and award new ones. Returns list of new badge keys."""
        new_badges = []
        existing = {a.badge_key for a in await self.repo.get_achievements(session_id)}

        # Get session stats
        from app.modules.mock_kankor.models import MockExamSession
        q = (
            select(MockExamSession)
            .where(
                MockExamSession.session_id == session_id,
                MockExamSession.completed_at.isnot(None),
            )
            .order_by(MockExamSession.created_at)
        )
        sessions = list((await self.db.execute(q)).scalars())

        if not sessions:
            return []

        total_exams = len(sessions)
        scores = [s.score or 0 for s in sessions]
        best_score = max(scores) if scores else 0

        # Check conditions
        checks = {
            "first_exam": total_exams >= 1,
            "five_exams": total_exams >= 5,
            "ten_exams": total_exams >= 10,
            "score_200": best_score >= (200 / 360 * 100),
            "score_280": best_score >= (280 / 360 * 100),
            "score_320": best_score >= (320 / 360 * 100),
        }

        # Streak check
        dates = sorted(set(s.created_at.date() for s in sessions))
        if len(dates) >= 3:
            streak = 1
            for i in range(len(dates) - 1, 0, -1):
                if (dates[i] - dates[i - 1]).days == 1:
                    streak += 1
                else:
                    break
            checks["streak_3"] = streak >= 3
            checks["streak_7"] = streak >= 7

        # Subject checks
        for s in sessions[-3:]:
            if s.subject_scores:
                for subj, data in s.subject_scores.items():
                    if subj == "ریاضی" and data.get("percentage", 0) >= 80:
                        checks["math_master"] = True
                    if subj in ("بیولوژی", "biology") and data.get("percentage", 0) >= 80:
                        checks["science_master"] = True

        # Award new badges
        for badge_key, condition in checks.items():
            if condition and badge_key not in existing:
                await self.repo.award(session_id, badge_key)
                new_badges.append(badge_key)

        return new_badges

    async def get_achievements(self, session_id: str) -> list[dict]:
        achievements = await self.repo.get_achievements(session_id)
        return [
            {
                "badge_key": a.badge_key,
                "name": BADGES.get(a.badge_key, {}).get("name", a.badge_key),
                "emoji": BADGES.get(a.badge_key, {}).get("emoji", "🏅"),
                "earned_at": a.earned_at.isoformat(),
            }
            for a in achievements
        ]

    async def get_leaderboard(self, days: int = 7) -> list[dict]:
        return await self.repo.get_leaderboard(days)
