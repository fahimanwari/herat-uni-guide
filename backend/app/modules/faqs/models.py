import uuid
from datetime import datetime

from sqlalchemy import String, Text, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Faq(Base):
    __tablename__ = "faqs"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    university_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("universities.id"), nullable=True
    )
    sort_order: Mapped[int] = mapped_column(Integer, default=0)
    category: Mapped[str | None] = mapped_column(String(100))

    question_fa: Mapped[str] = mapped_column(Text)
    answer_fa: Mapped[str] = mapped_column(Text)
    question_ps: Mapped[str | None] = mapped_column(Text)
    answer_ps: Mapped[str | None] = mapped_column(Text)
    question_en: Mapped[str | None] = mapped_column(Text)
    answer_en: Mapped[str | None] = mapped_column(Text)

    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        default=datetime.utcnow, onupdate=datetime.utcnow
    )
