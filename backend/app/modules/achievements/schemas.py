import uuid
from pydantic import BaseModel, ConfigDict


class AchievementSchema(BaseModel):
    """Matches the dict shape built in AchievementService.get_achievements —
    clients need the display name/emoji, not the row id."""

    badge_key: str
    name: str
    emoji: str
    earned_at: str


class LeaderboardEntry(BaseModel):
    rank: int
    score: float
    display_name: str
