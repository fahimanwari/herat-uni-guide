from datetime import datetime, timedelta

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .models import AcademicEvent


class EventRepository:

    def __init__(self, db: AsyncSession):
        self.db = db

    async def list_all(self) -> list[AcademicEvent]:
        q = select(AcademicEvent).order_by(AcademicEvent.event_date)
        return list((await self.db.execute(q)).scalars())

    async def events_needing_reminder(self, today: datetime) -> list[AcademicEvent]:
        """Events where event_date - remind_days_before <= today"""
        q = select(AcademicEvent).where(
            AcademicEvent.is_active == True,
            AcademicEvent.event_date - timedelta(days=AcademicEvent.remind_days_before) <= today,
            AcademicEvent.event_date >= today,
        )
        return list((await self.db.execute(q)).scalars())

    async def create(self, data: dict) -> AcademicEvent:
        obj = AcademicEvent(**data)
        self.db.add(obj)
        await self.db.commit()
        await self.db.refresh(obj)
        return obj
