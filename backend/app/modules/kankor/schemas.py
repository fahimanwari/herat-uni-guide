import uuid

from pydantic import BaseModel, ConfigDict


class CutoffSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    year: int
    min_score: float
    capacity: int | None


class CutoffCreate(BaseModel):
    year: int
    min_score: float
    capacity: int | None = None


class GuideListItem(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    title_fa: str
    category: str | None
    sort_order: int


class GuideDetail(GuideListItem):
    body_fa: str


class GuideCreate(BaseModel):
    title_fa: str
    body_fa: str
    category: str | None = None
    sort_order: int = 0


class ChanceResult(BaseModel):
    department_slug: str
    department_name: str
    department_type: str
    chance: str  # "high" | "medium" | "low"
    last_min_score: float
    avg_min_score: float
    trend: str  # "rising" | "stable" | "falling"
    cutoffs: list[CutoffSchema]
