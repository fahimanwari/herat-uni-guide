from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import get_db
from app.core.security import get_current_admin
from app.modules.admin_auth.models import AdminUser
from .repository import EventRepository
from .schemas import EventListItem, EventCreate

router = APIRouter(prefix="/notifications", tags=["notifications"])


@router.get("/events", response_model=list[EventListItem])
async def list_events(db: AsyncSession = Depends(get_db)):
    return await EventRepository(db).list_all()


@router.post("/events", response_model=EventListItem, status_code=201)
async def create_event(
    payload: EventCreate,
    db: AsyncSession = Depends(get_db),
    admin: AdminUser = Depends(get_current_admin),
):
    return await EventRepository(db).create(payload.model_dump())
