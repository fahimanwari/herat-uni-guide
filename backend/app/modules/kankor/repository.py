import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from .models import KankorCutoff, KankorGuide
from app.modules.departments.models import Department


class KankorRepository:

    def __init__(self, db: AsyncSession):
        self.db = db

    async def departments_with_cutoffs(self, department_type: str = "degree"):
        q = (
            select(Department)
            .options(selectinload(Department.cutoffs))
            .where(Department.department_type == department_type)
        )
        return list((await self.db.execute(q)).scalars())

    async def list_guides(self) -> list[KankorGuide]:
        q = select(KankorGuide).order_by(KankorGuide.sort_order)
        return list((await self.db.execute(q)).scalars())

    async def get_guide(self, id: uuid.UUID) -> KankorGuide | None:
        return await self.db.get(KankorGuide, id)

    async def create_guide(self, data: dict) -> KankorGuide:
        obj = KankorGuide(**data)
        self.db.add(obj)
        await self.db.commit()
        await self.db.refresh(obj)
        return obj

    # --- Cutoff CRUD ---

    async def list_cutoffs(self, department_id: uuid.UUID | None = None) -> list[KankorCutoff]:
        q = select(KankorCutoff).order_by(KankorCutoff.year.desc())
        if department_id:
            q = q.where(KankorCutoff.department_id == department_id)
        return list((await self.db.execute(q)).scalars())

    async def create_cutoff(self, data: dict) -> KankorCutoff:
        obj = KankorCutoff(**data)
        self.db.add(obj)
        await self.db.commit()
        await self.db.refresh(obj)
        return obj

    async def delete_cutoff(self, obj: KankorCutoff) -> None:
        await self.db.delete(obj)
        await self.db.commit()
