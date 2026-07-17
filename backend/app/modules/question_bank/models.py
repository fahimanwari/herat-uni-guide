import uuid
from datetime import datetime

from sqlalchemy import String, Text, Integer, Boolean, JSON
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class QuestionBank(Base):
    """Central question bank — questions are stored here and randomly selected for exams."""
    __tablename__ = "question_bank"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    subject: Mapped[str] = mapped_column(String(50), index=True)  # 'math', 'physics', 'chemistry', 'biology', 'dari', 'islamic', 'cs'
    difficulty: Mapped[str] = mapped_column(String(20), default="medium")  # 'easy', 'medium', 'hard'
    question_fa: Mapped[str] = mapped_column(Text)
    question_en: Mapped[str | None] = mapped_column(Text)
    options: Mapped[list] = mapped_column(JSON)  # [{"text": "...", "is_correct": true/false}]
    explanation_fa: Mapped[str | None] = mapped_column(Text)  # توضیح پاسخ صحیح
    source: Mapped[str | None] = mapped_column(String(100))  # 'kankor_1398', 'kankor_1399', etc.
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
