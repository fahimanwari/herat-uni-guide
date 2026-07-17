import uuid

from pydantic import BaseModel, ConfigDict


class OptionSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    text_fa: str


class QuestionSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    question_fa: str
    category: str | None
    sort_order: int
    options: list[OptionSchema]


class QuizMatch(BaseModel):
    department_slug: str
    department_name: str
    percent: int


class ScoreRequest(BaseModel):
    selected_option_ids: list[uuid.UUID]
