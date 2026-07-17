import uuid
from datetime import datetime

from sqlalchemy import String, Text, Integer, Float, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class KankorCutoff(Base):
    __tablename__ = "kankor_cutoffs"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    department_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("departments.id"))
    year: Mapped[int] = mapped_column(Integer)
    min_score: Mapped[float] = mapped_column(Float)
    capacity: Mapped[int | None] = mapped_column(Integer)

    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    department = relationship("Department", back_populates="cutoffs")


class KankorGuide(Base):
    __tablename__ = "kankor_guides"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    title_fa: Mapped[str] = mapped_column(String(300))
    body_fa: Mapped[str] = mapped_column(Text)
    category: Mapped[str | None] = mapped_column(String(100))
    sort_order: Mapped[int] = mapped_column(Integer, default=0)

    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
