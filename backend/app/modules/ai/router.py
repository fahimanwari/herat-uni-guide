from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
import redis.asyncio as aioredis

from app.core.deps import get_db
from app.config import settings
from .service import ChatService, ChatReply

router = APIRouter(prefix="/ai", tags=["ai"])


class ChatRequest(BaseModel):
    message: str
    language: str = "fa"
    session_id: str = ""


@router.post("/chat", response_model=ChatReply)
async def chat(payload: ChatRequest, db: AsyncSession = Depends(get_db)):
    redis_client = aioredis.from_url(settings.redis_url)
    try:
        service = ChatService(db, redis_client)
        return await service.ask(payload.message, payload.language)
    finally:
        await redis_client.aclose()
