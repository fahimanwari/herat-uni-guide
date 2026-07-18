import uuid
from pydantic import BaseModel, ConfigDict


class AchievementSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    badge_key: str
    earned_at: str


class LeaderboardEntry(BaseModel):
    rank: int
    score: float
    display_name: str
