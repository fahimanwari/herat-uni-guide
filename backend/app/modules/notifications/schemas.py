import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict


class EventListItem(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    title_fa: str
    event_date: datetime
    event_type: str
    remind_days_before: int


class EventDetail(EventListItem):
    description_fa: str | None
    is_active: bool


class EventCreate(BaseModel):
    title_fa: str
    description_fa: str | None = None
    event_date: datetime
    event_type: str
    remind_days_before: int = 3
    is_active: bool = True
