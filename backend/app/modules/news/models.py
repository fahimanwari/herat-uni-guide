import uuid
from datetime import datetime

from sqlalchemy import String, Text, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class News(Base):
    __tablename__ = "news"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    university_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("universities.id"))

    title_fa: Mapped[str] = mapped_column(String(300))
    title_ps: Mapped[str | None] = mapped_column(String(300))
    title_en: Mapped[str | None] = mapped_column(String(300))
    body_fa: Mapped[str] = mapped_column(Text)
    body_ps: Mapped[str | None] = mapped_column(Text)
    body_en: Mapped[str | None] = mapped_column(Text)

    cover_image_url: Mapped[str | None] = mapped_column(String(500))
    is_published: Mapped[bool] = mapped_column(Boolean, default=False)
    published_at: Mapped[datetime | None] = mapped_column(DateTime)
    send_notification: Mapped[bool] = mapped_column(Boolean, default=False)
    source_url: Mapped[str | None] = mapped_column(String(500), unique=True)
    is_ai_draft: Mapped[bool] = mapped_column(Boolean, default=False)

    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        default=datetime.utcnow, onupdate=datetime.utcnow
    )
