import uuid
import math

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from .models import QuizQuestion, QuizOption, DepartmentTraitProfile


TRAITS = ["logic", "biology", "language", "art", "social", "handson"]


def cosine_similarity(a: dict, b: dict) -> float:
    dot = sum(a.get(t, 0) * b.get(t, 0) for t in TRAITS)
    mag_a = math.sqrt(sum(a.get(t, 0) ** 2 for t in TRAITS))
    mag_b = math.sqrt(sum(b.get(t, 0) ** 2 for t in TRAITS))
    return dot / (mag_a * mag_b) if mag_a and mag_b else 0.0


class QuizRepository:

    def __init__(self, db: AsyncSession):
        self.db = db

    async def list_questions(self) -> list[QuizQuestion]:
        q = (
            select(QuizQuestion)
            .options(selectinload(QuizQuestion.options))
            .order_by(QuizQuestion.sort_order)
        )
        return list((await self.db.execute(q)).scalars())

    async def get_options(self, ids: list[uuid.UUID]) -> list[QuizOption]:
        q = select(QuizOption).where(QuizOption.id.in_(ids))
        return list((await self.db.execute(q)).scalars())

    async def all_profiles_with_departments(self):
        """پروفایل صفات + slug و نام رشته — فقط دیپارتمنت‌های فارغ‌ده"""
        from app.modules.departments.models import Department

        q = (
            select(DepartmentTraitProfile, Department.slug, Department.name_fa)
            .join(Department, Department.id == DepartmentTraitProfile.department_id)
            .where(Department.department_type == "degree")
        )
        return list((await self.db.execute(q)).all())

    # --- Profile CRUD ---

    async def list_profiles(self) -> list[DepartmentTraitProfile]:
        q = select(DepartmentTraitProfile).order_by(DepartmentTraitProfile.id)
        return list((await self.db.execute(q)).scalars())

    async def get_profile(self, id: uuid.UUID) -> DepartmentTraitProfile | None:
        return await self.db.get(DepartmentTraitProfile, id)

    async def create_profile(self, data: dict) -> DepartmentTraitProfile:
        obj = DepartmentTraitProfile(**data)
        self.db.add(obj)
        await self.db.commit()
        await self.db.refresh(obj)
        return obj

    async def update_profile(self, obj: DepartmentTraitProfile, data: dict) -> DepartmentTraitProfile:
        for key, value in data.items():
            setattr(obj, key, value)
        await self.db.commit()
        await self.db.refresh(obj)
        return obj

    async def delete_profile(self, obj: DepartmentTraitProfile) -> None:
        await self.db.delete(obj)
        await self.db.commit()
