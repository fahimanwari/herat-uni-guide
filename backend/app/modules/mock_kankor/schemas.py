import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, field_validator


class StartMockExamRequest(BaseModel):
    session_id: str
    subject: str | None = None  # None = all subjects
    num_questions: int = 160
    year_filter: int | None = None  # Filter by year
    blueprint_id: str | None = None  # If set, sample per-subject sections instead of flat random


class ExamBlueprintSection(BaseModel):
    subject: str
    count: int


class ExamBlueprintItem(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    name_fa: str
    description_fa: str | None = None
    total_minutes: int
    sections: list[ExamBlueprintSection]
    is_active: bool = True

    @field_validator("sections")
    @classmethod
    def check_sections(cls, v):
        if not v:
            raise ValueError("حداقل یک بخش (مضمون) لازم است")
        return v


class ExamBlueprintCreate(BaseModel):
    name_fa: str
    description_fa: str | None = None
    total_minutes: int = 160
    sections: list[ExamBlueprintSection]
    is_active: bool = True

    @field_validator("sections")
    @classmethod
    def check_sections(cls, v):
        if not v:
            raise ValueError("حداقل یک بخش (مضمون) لازم است")
        return v


class MockQuestionSchema(BaseModel):
    id: str
    question_fa: str
    options: list[dict]  # [{"id": "...", "text": "..."}]
    subject: str
    sort_order: int


class MockExamStartResponse(BaseModel):
    session_id: str
    questions: list[MockQuestionSchema]
    total_questions: int
    total_minutes: int


class SubmitMockExamRequest(BaseModel):
    answers: dict[str, str]  # {question_id: option_id}
    time_taken_seconds: int | None = None


class MockExamResult(BaseModel):
    session_id: str
    score: float
    score_360: float  # نمره تخمینی به مقیاس کانکور واقعی (از ۳۶۰)
    correct_answers: int
    wrong_answers: int
    empty_answers: int
    total_answers: int
    subject_scores: dict
    passed: bool
    time_taken_seconds: int | None


class MockExamReview(BaseModel):
    session_id: str
    questions: list[dict]  # [{question, user_answer, correct_answer, is_correct, explanation}]
    score: float
    subject_scores: dict
