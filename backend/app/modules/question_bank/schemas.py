import uuid

from pydantic import BaseModel, ConfigDict


class QuestionBankItem(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    subject: str
    difficulty: str
    question_fa: str
    options: list[dict]
    source: str | None


class QuestionBankCreate(BaseModel):
    subject: str
    difficulty: str = "medium"
    question_fa: str
    options: list[dict] = []
    source: str | None = None
    explanation_fa: str | None = None


class GenerateExamRequest(BaseModel):
    subject: str | None = None  # None = random from all
    num_questions: int = 10
    difficulty: str | None = None  # None = mixed


class GeneratedQuestion(BaseModel):
    id: str
    question_fa: str
    options: list[dict]  # [{"id": "...", "text": "..."}]
    sort_order: int
    points: int
