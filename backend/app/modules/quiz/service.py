import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .repository import QuizRepository, cosine_similarity
from .schemas import QuizMatch


class QuizService:

    def __init__(self, db: AsyncSession):
        self.repo = QuizRepository(db)

    async def get_questions(self):
        return await self.repo.list_questions()

    async def score(self, selected_option_ids: list[uuid.UUID]) -> list[QuizMatch]:
        # 1. Sum weights of selected options -> user interest vector
        user_vector: dict[str, int] = {}
        for opt in await self.repo.get_options(selected_option_ids):
            for trait, w in opt.trait_weights.items():
                user_vector[trait] = user_vector.get(trait, 0) + w

        # 2. Cosine similarity with each degree-department profile
        matches = []
        for profile, slug, name_fa in await self.repo.all_profiles_with_departments():
            sim = cosine_similarity(user_vector, profile.trait_weights)
            matches.append(QuizMatch(
                department_slug=slug,
                department_name=name_fa,
                percent=round(sim * 100),
            ))
        return sorted(matches, key=lambda m: -m.percent)[:5]

    # --- CRUD ---

    async def create_question(self, payload):
        data = payload.model_dump()
        data["id"] = uuid.uuid4()
        from .models import QuizQuestion
        obj = QuizQuestion(**data)
        self.repo.db.add(obj)
        await self.repo.db.commit()
        await self.repo.db.refresh(obj)
        return obj

    async def update_question(self, id: uuid.UUID, payload):
        from .models import QuizQuestion
        q = select(QuizQuestion).where(QuizQuestion.id == id)
        obj = (await self.repo.db.execute(q)).scalar_one_or_none()
        if obj is None:
            from app.core.exceptions import NotFoundError
            raise NotFoundError("سوال یافت نشد")
        for key, value in payload.model_dump(exclude_unset=True).items():
            setattr(obj, key, value)
        await self.repo.db.commit()
        await self.repo.db.refresh(obj)
        return obj

    async def delete_question(self, id: uuid.UUID):
        from .models import QuizQuestion
        q = select(QuizQuestion).where(QuizQuestion.id == id)
        obj = (await self.repo.db.execute(q)).scalar_one_or_none()
        if obj is None:
            from app.core.exceptions import NotFoundError
            raise NotFoundError("سوال یافت نشد")
        await self.repo.db.delete(obj)
        await self.repo.db.commit()

    # --- Profile CRUD ---

    async def list_profiles(self):
        return await self.repo.list_profiles()

    async def get_profile(self, id: uuid.UUID):
        from app.core.exceptions import NotFoundError
        profile = await self.repo.get_profile(id)
        if profile is None:
            raise NotFoundError("پروفایل صفات یافت نشد")
        return profile

    async def create_profile(self, payload):
        return await self.repo.create_profile(payload.model_dump())

    async def update_profile(self, id: uuid.UUID, payload):
        from app.core.exceptions import NotFoundError
        profile = await self.repo.get_profile(id)
        if profile is None:
            raise NotFoundError("پروفایل صفات یافت نشد")
        return await self.repo.update_profile(profile, payload.model_dump(exclude_unset=True))

    async def delete_profile(self, id: uuid.UUID):
        from app.core.exceptions import NotFoundError
        profile = await self.repo.get_profile(id)
        if profile is None:
            raise NotFoundError("پروفایل صفات یافت نشد")
        await self.repo.delete_profile(profile)
