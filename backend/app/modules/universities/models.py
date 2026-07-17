import uuid
from datetime import datetime

from sqlalchemy import String, Text, Integer, Boolean, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class University(Base):
    __tablename__ = "universities"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    slug: Mapped[str] = mapped_column(String(100), unique=True, index=True)

    # Three-language: Dari required, Pashto/English optional
    name_fa: Mapped[str] = mapped_column(String(200))
    name_ps: Mapped[str | None] = mapped_column(String(200))
    name_en: Mapped[str | None] = mapped_column(String(200))

    description_fa: Mapped[str] = mapped_column(Text)
    description_ps: Mapped[str | None] = mapped_column(Text)
    description_en: Mapped[str | None] = mapped_column(Text)

    history_fa: Mapped[str | None] = mapped_column(Text)
    chancellor_name: Mapped[str | None] = mapped_column(String(200))
    logo_url: Mapped[str | None] = mapped_column(String(500))
    established_year: Mapped[int | None] = mapped_column(Integer)
    stats: Mapped[dict | None] = mapped_column(JSON, default=dict)
    lat: Mapped[float | None] = mapped_column()
    lng: Mapped[float | None] = mapped_column()
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        default=datetime.utcnow, onupdate=datetime.utcnow
    )

    faculties = relationship("Faculty", back_populates="university")
