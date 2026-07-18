import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import NotFoundError
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
                data_year=cutoffs[-1].year,
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

    # --- CRUD ---

    async def list_cutoffs(self, department_id: uuid.UUID | None = None):
        return await self.repo.list_cutoffs(department_id)

    async def create_cutoff(self, department_id: uuid.UUID, payload):
        data = payload.model_dump()
        data["id"] = uuid.uuid4()
        data["department_id"] = department_id
        return await self.repo.create_cutoff(data)

    async def delete_cutoff(self, id: uuid.UUID):
        from .models import KankorCutoff
        from sqlalchemy import select
        q = select(KankorCutoff).where(KankorCutoff.id == id)
        obj = (await self.repo.db.execute(q)).scalar_one_or_none()
        if obj is None:
            raise NotFoundError("کات‌آف یافت نشد")
        await self.repo.delete_cutoff(obj)

    async def update_cutoff(self, id: uuid.UUID, payload):
        from .models import KankorCutoff
        from sqlalchemy import select
        q = select(KankorCutoff).where(KankorCutoff.id == id)
        obj = (await self.repo.db.execute(q)).scalar_one_or_none()
        if obj is None:
            raise NotFoundError("کات‌آف یافت نشد")
        return await self.repo.update_cutoff(obj, payload.model_dump(exclude_unset=True))

    # --- Guide CRUD ---

    async def list_guides(self):
        return await self.repo.list_guides()

    async def get_guide(self, id: uuid.UUID):
        guide = await self.repo.get_guide(id)
        if guide is None:
            raise NotFoundError("راهنما یافت نشد")
        return guide

    async def create_guide(self, payload):
        return await self.repo.create_guide(payload.model_dump())

    async def update_guide(self, id: uuid.UUID, payload):
        guide = await self.get_guide(id)
        return await self.repo.update_guide(guide, payload.model_dump(exclude_unset=True))

    async def delete_guide(self, id: uuid.UUID):
        guide = await self.get_guide(id)
        await self.repo.delete_guide(guide)
