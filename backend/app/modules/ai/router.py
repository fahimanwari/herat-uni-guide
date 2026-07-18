from fastapi import APIRouter, Depends, Request, UploadFile, File
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


class StudyPlanRequest(BaseModel):
    session_id: str


@router.post("/study-plan")
async def study_plan(payload: StudyPlanRequest, request: Request, db: AsyncSession = Depends(get_db)):
    client_ip = request.client.host
    await rate_limiter.check_rate_limit(f"plan:{client_ip}", limit=5, window=86400)
    from .study_plan import StudyPlanService
    return await StudyPlanService(db).generate(payload.session_id)


@router.post("/transcribe")
async def transcribe_audio(
    file: UploadFile = File(...),
    request: Request = None,
):
    """Transcribe audio using Groq Whisper."""
    if request:
        client_ip = request.client.host
        await rate_limiter.check_rate_limit(f"transcribe:{client_ip}", limit=20, window=86400)

    import httpx
    audio_bytes = await file.read()

    async with httpx.AsyncClient(timeout=60) as client:
        r = await client.post(
            "https://api.groq.com/openai/v1/audio/transcriptions",
            headers={"Authorization": f"Bearer {settings.ai_api_key}"},
            files={"file": (file.filename, audio_bytes, file.content_type or "audio/webm")},
            data={"model": "whisper-large-v3"},
        )
        r.raise_for_status()
        return {"text": r.json().get("text", "")}
