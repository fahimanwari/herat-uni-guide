import uuid
from datetime import datetime

from sqlalchemy import String, Text, Integer, Boolean, JSON
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class QuestionBank(Base):
    """Central question bank — questions are stored here and randomly selected for exams."""
    __tablename__ = "question_bank"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    subject: Mapped[str] = mapped_column(String(50), index=True)
    difficulty: Mapped[str] = mapped_column(String(20), default="medium")
    question_fa: Mapped[str] = mapped_column(Text)
    question_en: Mapped[str | None] = mapped_column(Text)
    options: Mapped[list] = mapped_column(JSON)  # [{"text": "...", "is_correct": true/false}]
    explanation_fa: Mapped[str | None] = mapped_column(Text)
    source: Mapped[str | None] = mapped_column(String(100))
    year: Mapped[int | None] = mapped_column(Integer, index=True)  # سال کانکور: ۱۳۹۸...۱۴۰۵
    grade: Mapped[str | None] = mapped_column(String(10), index=True)  # صنف کتاب درسی: "10" | "11" | "12"
    chapter: Mapped[str | None] = mapped_column(String(150))  # فصل/باب کتاب درسی
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)


class ExamBlueprint(Base):
    """Structure for standardized mock exams."""
    __tablename__ = "exam_blueprints"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    name_fa: Mapped[str] = mapped_column(String(300))
    description_fa: Mapped[str | None] = mapped_column(Text)
    total_minutes: Mapped[int] = mapped_column(Integer, default=160)
    sections: Mapped[list] = mapped_column(JSON)
    # [{"subject":"ریاضی","count":30},{"subject":"فزیک","count":25},...]
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
