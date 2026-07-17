import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict


class OptionSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    text_fa: str
    text_en: str | None


class QuestionSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    question_fa: str
    question_en: str | None
    sort_order: int
    points: int
    options: list[OptionSchema]


class ExamListItem(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    title_fa: str
    title_en: str | None
    category: str
    duration_minutes: int
    total_questions: int


class ExamDetail(ExamListItem):
    description_fa: str | None


class ExamWithQuestions(ExamDetail):
    questions: list[QuestionSchema]


class SubmitExamRequest(BaseModel):
    session_id: str
    answers: dict[str, str]  # {question_id: option_id}
    time_taken_seconds: int | None = None


class ExamResultResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    exam_id: uuid.UUID
    score: float
    total_points: int
    correct_answers: int
    total_answers: int
    percentage: float
    time_taken_seconds: int | None
    created_at: datetime


class ExamResultDetail(ExamResultResponse):
    answers: dict
    exam_title: str
