import uuid

from pydantic import BaseModel, ConfigDict


class FaqListItem(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    question_fa: str
    category: str | None
    sort_order: int


class FaqDetail(FaqListItem):
    answer_fa: str
    question_ps: str | None
    answer_ps: str | None
    question_en: str | None
    answer_en: str | None


class FaqCreate(BaseModel):
    university_id: uuid.UUID | None = None
    question_fa: str
    answer_fa: str
    category: str | None = None
    sort_order: int = 0
    question_ps: str | None = None
    answer_ps: str | None = None
    question_en: str | None = None
    answer_en: str | None = None


class FaqUpdate(BaseModel):
    question_fa: str | None = None
    answer_fa: str | None = None
    category: str | None = None
    sort_order: int | None = None
    question_ps: str | None = None
    answer_ps: str | None = None
    question_en: str | None = None
    answer_en: str | None = None
