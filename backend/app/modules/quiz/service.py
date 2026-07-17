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

        # 2. Cosine similarity with each department profile
        matches = []
        for profile in await self.repo.all_profiles():
            sim = cosine_similarity(user_vector, profile.trait_weights)
            # Get department name from relationship if available
            dept_name = profile.department_id  # fallback
            matches.append(QuizMatch(
                department_slug=str(profile.department_id),
                department_name=dept_name,
                percent=round(sim * 100),
            ))
        return sorted(matches, key=lambda m: -m.percent)[:5]
