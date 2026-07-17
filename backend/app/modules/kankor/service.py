from sqlalchemy.ext.asyncio import AsyncSession

from .repository import KankorRepository
from .schemas import ChanceResult


class KankorService:

    def __init__(self, db: AsyncSession):
        self.repo = KankorRepository(db)

    async def calculate_chances(self, score: float) -> list[ChanceResult]:
        """User estimated score -> chance of admission — only degree departments"""
        results = []
        for dept in await self.repo.departments_with_cutoffs(department_type="degree"):
            cutoffs = sorted(dept.cutoffs, key=lambda c: c.year)
            if not cutoffs:
                continue

            last = cutoffs[-1].min_score
            avg = sum(c.min_score for c in cutoffs) / len(cutoffs)

            if score >= last + 10:
                chance = "high"
            elif score >= last - 5:
                chance = "medium"
            else:
                chance = "low"

            trend = self._trend(cutoffs)
            results.append(ChanceResult(
                department_slug=dept.slug,
                department_name=dept.name_fa,
                department_type=dept.department_type,
                chance=chance,
                last_min_score=last,
                avg_min_score=round(avg, 1),
                trend=trend,
                cutoffs=sorted(cutoffs, key=lambda c: c.year),
            ))

        order = {"high": 0, "medium": 1, "low": 2}
        return sorted(results, key=lambda r: order[r.chance])

    def _trend(self, cutoffs) -> str:
        if len(cutoffs) < 2:
            return "stable"
        diff = cutoffs[-1].min_score - cutoffs[-2].min_score
        if diff > 3:
            return "rising"
        if diff < -3:
            return "falling"
        return "stable"
