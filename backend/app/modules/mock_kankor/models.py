import uuid
from datetime import datetime

from sqlalchemy import String, Text, Integer, Float, ForeignKey, JSON, Boolean, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class MockExamSession(Base):
    """A user's mock exam session."""
    __tablename__ = "mock_exam_sessions"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    session_id: Mapped[str] = mapped_column(String(100), index=True)
    user_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("users.id"), nullable=True)
    blueprint_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("exam_blueprints.id", ondelete="SET NULL"), nullable=True
    )
    questions: Mapped[list] = mapped_column(JSON)  # Selected question IDs
    answers: Mapped[dict] = mapped_column(JSON, default=dict)  # {question_id: option_id}
    started_at: Mapped[datetime] = mapped_column(DateTime)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime)
    score: Mapped[float | None] = mapped_column(Float)
    subject_scores: Mapped[dict] = mapped_column(JSON, default=dict)
    time_taken_seconds: Mapped[int | None] = mapped_column(Integer)

    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
