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
    subject: str | None
    options: list[OptionSchema]


class ExamListItem(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    title_fa: str
    title_en: str | None
    category: str
    year: int | None
    duration_minutes: int
    total_questions: int
    passing_score: float


class ExamCreate(BaseModel):
    title_fa: str
    title_en: str | None = None
    category: str = "kankor"
    year: int | None = None
    duration_minutes: int = 60
    total_questions: int = 10
    passing_score: float = 50.0
    description_fa: str | None = None
    max_score: float = 100.0


class ExamDetail(ExamListItem):
    description_fa: str | None
    max_score: float


class ExamWithQuestions(ExamDetail):
    questions: list[QuestionSchema]


class SubmitExamRequest(BaseModel):
    session_id: str
    user_id: str | None = None
    answers: dict[str, str]  # {question_id: option_id}
    time_taken_seconds: int | None = None
    started_at: str | None = None


class SubjectScore(BaseModel):
    subject: str
    correct: int
    total: int
    percentage: float


class ExamResultResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    exam_id: uuid.UUID
    score: float
    raw_score: float
    correct_answers: int
    wrong_answers: int
    empty_answers: int
    total_answers: int
    subject_scores: dict
    percentage: float
    passed: bool
    time_taken_seconds: int | None
    compared_to_avg: float | None
    created_at: datetime


class ExamResultDetail(ExamResultResponse):
    answers: dict
    exam_title: str
    exam_year: int | None


class UserStats(BaseModel):
    total_exams: int
    average_score: float
    best_score: float
    worst_score: float
    total_time_minutes: int
    subject_averages: dict
    improvement_trend: str  # 'improving', 'stable', 'declining'
    rank_estimate: str  # 'top 10%', 'top 25%', etc.
