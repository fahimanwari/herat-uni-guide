import uuid
from datetime import datetime

from sqlalchemy import String, Text, Integer, Float, ForeignKey, JSON, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Exam(Base):
    __tablename__ = "exams"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    title_fa: Mapped[str] = mapped_column(String(300))
    title_en: Mapped[str | None] = mapped_column(String(300))
    description_fa: Mapped[str | None] = mapped_column(Text)
    category: Mapped[str] = mapped_column(String(100))  # 'kankor', 'department', 'general'
    duration_minutes: Mapped[int] = mapped_column(Integer, default=60)
    total_questions: Mapped[int] = mapped_column(Integer, default=0)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    questions = relationship("ExamQuestion", back_populates="exam")
    results = relationship("ExamResult", back_populates="exam")


class ExamQuestion(Base):
    __tablename__ = "exam_questions"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    exam_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("exams.id"))
    question_fa: Mapped[str] = mapped_column(Text)
    question_en: Mapped[str | None] = mapped_column(Text)
    sort_order: Mapped[int] = mapped_column(Integer, default=0)
    points: Mapped[int] = mapped_column(Integer, default=1)

    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    exam = relationship("Exam", back_populates="questions")
    options = relationship("ExamOption", back_populates="question")


class ExamOption(Base):
    __tablename__ = "exam_options"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    question_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("exam_questions.id"))
    text_fa: Mapped[str] = mapped_column(String(500))
    text_en: Mapped[str | None] = mapped_column(String(500))
    is_correct: Mapped[bool] = mapped_column(Boolean, default=False)

    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    question = relationship("ExamQuestion", back_populates="options")


class ExamResult(Base):
    __tablename__ = "exam_results"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    exam_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("exams.id"))
    session_id: Mapped[str] = mapped_column(String(100))
    score: Mapped[float] = mapped_column(Float, default=0)
    total_points: Mapped[int] = mapped_column(Integer, default=0)
    correct_answers: Mapped[int] = mapped_column(Integer, default=0)
    total_answers: Mapped[int] = mapped_column(Integer, default=0)
    answers: Mapped[dict] = mapped_column(JSON, default=dict)
    # {"question_id": "option_id", ...}
    time_taken_seconds: Mapped[int | None] = mapped_column(Integer)

    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    exam = relationship("Exam", back_populates="results")
