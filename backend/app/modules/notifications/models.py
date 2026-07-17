import uuid
from datetime import datetime

from sqlalchemy import String, Text, Integer, Date, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class AcademicEvent(Base):
    __tablename__ = "academic_events"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    title_fa: Mapped[str] = mapped_column(String(300))
    description_fa: Mapped[str | None] = mapped_column(Text)
    event_date: Mapped[datetime] = mapped_column(Date)
    event_type: Mapped[str] = mapped_column(String(50))
    # 'kankor_registration', 'kankor_exam', 'kankor_results', 'semester_start', 'other'
    remind_days_before: Mapped[int] = mapped_column(Integer, default=3)
    is_active: Mapped[bool] = mapped_column(default=True)

    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
