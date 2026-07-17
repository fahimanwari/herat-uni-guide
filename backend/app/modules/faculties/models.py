import uuid
from datetime import datetime

from sqlalchemy import String, Text, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Faculty(Base):
    __tablename__ = "faculties"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    university_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("universities.id"))
    slug: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    sort_order: Mapped[int] = mapped_column(Integer, default=0)

    name_fa: Mapped[str] = mapped_column(String(200))
    name_ps: Mapped[str | None] = mapped_column(String(200))
    name_en: Mapped[str | None] = mapped_column(String(200))

    description_fa: Mapped[str] = mapped_column(Text)
    description_ps: Mapped[str | None] = mapped_column(Text)
    description_en: Mapped[str | None] = mapped_column(Text)

    vision_fa: Mapped[str | None] = mapped_column(Text)
    mission_fa: Mapped[str | None] = mapped_column(Text)

    cover_image_url: Mapped[str | None] = mapped_column(String(500))
    youtube_video_id: Mapped[str | None] = mapped_column(String(50))
    dean_name: Mapped[str | None] = mapped_column(String(200))
    established_year: Mapped[int | None] = mapped_column(Integer)

    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        default=datetime.utcnow, onupdate=datetime.utcnow
    )

    university = relationship("University", back_populates="faculties")
    departments = relationship("Department", back_populates="faculty")
