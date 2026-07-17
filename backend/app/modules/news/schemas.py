import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict


class NewsListItem(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    title_fa: str
    title_en: str | None
    cover_image_url: str | None
    published_at: datetime | None


class NewsDetail(NewsListItem):
    university_id: uuid.UUID
    title_ps: str | None
    body_fa: str
    body_ps: str | None
    body_en: str | None


class NewsCreate(BaseModel):
    university_id: uuid.UUID
    title_fa: str
    body_fa: str
    title_ps: str | None = None
    title_en: str | None = None
    body_ps: str | None = None
    body_en: str | None = None
    cover_image_url: str | None = None
    is_published: bool = False
    send_notification: bool = False


class NewsUpdate(BaseModel):
    title_fa: str | None = None
    body_fa: str | None = None
    title_ps: str | None = None
    title_en: str | None = None
    body_ps: str | None = None
    body_en: str | None = None
    cover_image_url: str | None = None
    is_published: bool | None = None
    send_notification: bool | None = None
