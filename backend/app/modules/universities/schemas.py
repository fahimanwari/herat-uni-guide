import uuid

from pydantic import BaseModel, ConfigDict


class UniversityListItem(BaseModel):
    """For lists — lightweight"""
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    slug: str
    name_fa: str
    name_en: str | None
    established_year: int | None
    logo_url: str | None


class UniversityDetail(UniversityListItem):
    """For detail page — full"""
    name_ps: str | None
    description_fa: str
    description_ps: str | None
    description_en: str | None
    history_fa: str | None
    chancellor_name: str | None
    stats: dict | None
    lat: float | None
    lng: float | None


class UniversityCreate(BaseModel):
    slug: str
    name_fa: str
    description_fa: str
    name_ps: str | None = None
    name_en: str | None = None
    description_ps: str | None = None
    description_en: str | None = None
    history_fa: str | None = None
    chancellor_name: str | None = None
    logo_url: str | None = None
    established_year: int | None = None
    stats: dict | None = None
    lat: float | None = None
    lng: float | None = None


class UniversityUpdate(BaseModel):
    name_fa: str | None = None
    description_fa: str | None = None
    name_ps: str | None = None
    name_en: str | None = None
    description_ps: str | None = None
    description_en: str | None = None
    history_fa: str | None = None
    chancellor_name: str | None = None
    logo_url: str | None = None
    established_year: int | None = None
    stats: dict | None = None
    lat: float | None = None
    lng: float | None = None
    is_active: bool | None = None
