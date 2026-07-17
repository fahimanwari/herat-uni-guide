import uuid

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
