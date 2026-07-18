import uuid

from pydantic import BaseModel, ConfigDict, field_validator


class QuestionOption(BaseModel):
    text: str
    is_correct: bool = False


def _validate_options(options: list[QuestionOption]) -> list[QuestionOption]:
    if len(options) < 2:
        raise ValueError("حداقل ۲ گزینه لازم است")
    if sum(1 for o in options if o.is_correct) != 1:
        raise ValueError("دقیقاً یک گزینه باید به‌عنوان جواب درست مشخص شود")
    return options


_VALID_GRADES = {"10", "11", "12"}


def _validate_grade(v: str | None) -> str | None:
    if v is not None and v not in _VALID_GRADES:
        raise ValueError("صنف باید 10، 11 یا 12 باشد")
    return v


class QuestionBankItem(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    subject: str
    difficulty: str
    question_fa: str
    options: list[QuestionOption]
    source: str | None = None
    year: int | None = None
    grade: str | None = None
    chapter: str | None = None
    is_verified: bool = False
    explanation_fa: str | None = None

    @field_validator("options")
    @classmethod
    def check_options(cls, v):
        return _validate_options(v)

    @field_validator("grade")
    @classmethod
    def check_grade(cls, v):
        return _validate_grade(v)


class QuestionBankCreate(BaseModel):
    subject: str
    difficulty: str = "medium"
    question_fa: str
    options: list[QuestionOption] = []
    source: str | None = None
    explanation_fa: str | None = None
    year: int | None = None
    grade: str | None = None
    chapter: str | None = None
    is_verified: bool = False

    @field_validator("options")
    @classmethod
    def check_options(cls, v):
        return _validate_options(v)

    @field_validator("grade")
    @classmethod
    def check_grade(cls, v):
        return _validate_grade(v)


class QuestionBankImportItem(BaseModel):
    """Strict schema for bulk import — one JSON row from scripts/question_format.json."""

    subject: str
    difficulty: str = "medium"
    question_fa: str
    question_en: str | None = None
    options: list[QuestionOption]
    explanation_fa: str | None = None
    source: str | None = None
    year: int | None = None
    grade: str | None = None
    chapter: str | None = None
    is_verified: bool = False

    @field_validator("options")
    @classmethod
    def check_options(cls, v):
        return _validate_options(v)

    @field_validator("grade")
    @classmethod
    def check_grade(cls, v):
        return _validate_grade(v)


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
