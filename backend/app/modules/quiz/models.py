import uuid
from datetime import datetime

from sqlalchemy import String, Text, Integer, ForeignKey, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class QuizQuestion(Base):
    __tablename__ = "quiz_questions"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    question_fa: Mapped[str] = mapped_column(Text)
    category: Mapped[str | None] = mapped_column(String(100))
    sort_order: Mapped[int] = mapped_column(Integer, default=0)

    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    options = relationship("QuizOption", back_populates="question")


class QuizOption(Base):
    __tablename__ = "quiz_options"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    question_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("quiz_questions.id"))
    text_fa: Mapped[str] = mapped_column(String(300))
    trait_weights: Mapped[dict] = mapped_column(JSON, default=dict)
    # {"logic":3,"biology":0,"language":1,"art":0,"social":1,"handson":0}

    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    question = relationship("QuizQuestion", back_populates="options")


class DepartmentTraitProfile(Base):
    __tablename__ = "department_trait_profiles"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    department_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("departments.id"), unique=True)
    trait_weights: Mapped[dict] = mapped_column(JSON, default=dict)
    # {"logic":3,"biology":0,"language":1,"art":0,"social":1,"handson":2}

    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
