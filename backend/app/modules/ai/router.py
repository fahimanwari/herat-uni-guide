from fastapi import APIRouter, Depends, Request
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
import redis.asyncio as aioredis

from app.core.deps import get_db
from app.config import settings
from app.core.rate_limit import rate_limiter
from .service import ChatService, ChatReply

router = APIRouter(prefix="/ai", tags=["ai"])


class ChatRequest(BaseModel):
    message: str
    language: str = "fa"
    session_id: str = ""


@router.post("/chat", response_model=ChatReply)
async def chat(payload: ChatRequest, request: Request, db: AsyncSession = Depends(get_db)):
    # Rate limit: 20 AI messages per day per IP
    client_ip = request.client.host
    await rate_limiter.check_rate_limit(f"ai:{client_ip}", limit=20, window=86400)

    redis_client = aioredis.from_url(settings.redis_url)
    try:
        service = ChatService(db, redis_client)
        return await service.ask(payload.message, payload.language)
    finally:
        await redis_client.aclose()
