import uuid

from pydantic import BaseModel, ConfigDict


class FacultyListItem(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    slug: str
    name_fa: str
    name_en: str | None
    cover_image_url: str | None
    sort_order: int


class FacultyDetail(FacultyListItem):
    university_id: uuid.UUID
    name_ps: str | None
    description_fa: str
    description_ps: str | None
    description_en: str | None
    vision_fa: str | None
    mission_fa: str | None
    youtube_video_id: str | None
    dean_name: str | None
    established_year: int | None


class FacultyCreate(BaseModel):
    university_id: uuid.UUID
    slug: str
    name_fa: str
    description_fa: str
    name_ps: str | None = None
    name_en: str | None = None
    description_ps: str | None = None
    description_en: str | None = None
    vision_fa: str | None = None
    mission_fa: str | None = None
    cover_image_url: str | None = None
    youtube_video_id: str | None = None
    dean_name: str | None = None
    established_year: int | None = None
    sort_order: int = 0


class FacultyUpdate(BaseModel):
    name_fa: str | None = None
    description_fa: str | None = None
    name_ps: str | None = None
    name_en: str | None = None
    description_ps: str | None = None
    description_en: str | None = None
    vision_fa: str | None = None
    mission_fa: str | None = None
    cover_image_url: str | None = None
    youtube_video_id: str | None = None
    dean_name: str | None = None
    established_year: int | None = None
    sort_order: int | None = None
