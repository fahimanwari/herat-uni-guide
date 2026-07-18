import uuid
from datetime import datetime

from sqlalchemy import String, Text, Integer, Float, ForeignKey, JSON, Boolean, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Exam(Base):
    __tablename__ = "exams"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    title_fa: Mapped[str] = mapped_column(String(300))
    title_en: Mapped[str | None] = mapped_column(String(300))
    description_fa: Mapped[str | None] = mapped_column(Text)
    category: Mapped[str] = mapped_column(String(100))  # 'kankor', 'department', 'general'
    year: Mapped[int | None] = mapped_column(Integer)  # سال امتحان (مثلاً 1404)
    duration_minutes: Mapped[int] = mapped_column(Integer, default=60)
    total_questions: Mapped[int] = mapped_column(Integer, default=0)
    passing_score: Mapped[float] = mapped_column(Float, default=50.0)  # نمره قبولی
    max_score: Mapped[float] = mapped_column(Float, default=100.0)  # بیشترین نمره
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    questions = relationship("ExamQuestion", back_populates="exam", cascade="all, delete-orphan")
    results = relationship("ExamResult", back_populates="exam", cascade="all, delete-orphan")


class ExamQuestion(Base):
    __tablename__ = "exam_questions"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    exam_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("exams.id"))
    question_fa: Mapped[str] = mapped_column(Text)
    question_en: Mapped[str | None] = mapped_column(Text)
    sort_order: Mapped[int] = mapped_column(Integer, default=0)
    points: Mapped[int] = mapped_column(Integer, default=1)
    subject: Mapped[str | None] = mapped_column(String(50))  # 'math', 'physics', etc.

    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    exam = relationship("Exam", back_populates="questions")
    options = relationship("ExamOption", back_populates="question", cascade="all, delete-orphan")


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
    user_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("users.id"), nullable=True)
    session_id: Mapped[str] = mapped_column(String(100))

    # Scoring
    score: Mapped[float] = mapped_column(Float, default=0)  # نمره از 100
    raw_score: Mapped[float] = mapped_column(Float, default=0)  # نمره خام
    total_points: Mapped[int] = mapped_column(Integer, default=0)
    correct_answers: Mapped[int] = mapped_column(Integer, default=0)
    wrong_answers: Mapped[int] = mapped_column(Integer, default=0)
    empty_answers: Mapped[int] = mapped_column(Integer, default=0)
    total_answers: Mapped[int] = mapped_column(Integer, default=0)

    # Subject scores
    subject_scores: Mapped[dict] = mapped_column(JSON, default=dict)
    # {"math": 80, "physics": 60, ...}

    # Detailed answers
    answers: Mapped[dict] = mapped_column(JSON, default=dict)
    # {"question_id": {"selected": "option_id", "correct": "option_id", "is_correct": true}}

    # Timing
    time_taken_seconds: Mapped[int | None] = mapped_column(Integer)
    started_at: Mapped[datetime | None] = mapped_column(DateTime)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime)

    # Year comparison
    exam_year: Mapped[int | None] = mapped_column(Integer)
    compared_to_avg: Mapped[float | None] = mapped_column(Float)  # درصد بهتر از میانگین

    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    exam = relationship("Exam", back_populates="results")
    user = relationship("User")
