from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from .retriever import RagRetriever
from .cache import ChatCache
from app.providers.ai.factory import get_ai_provider


SYSTEM_PROMPT = """تو دستیار هوشمند پوهنتون هرات هستی. فقط بر اساس «اطلاعات دانشگاه»
زیر جواب بده. اگر جواب در اطلاعات نبود، صادقانه بگو نمی‌دانی و پیشنهاد کن
با دانشگاه تماس بگیرند. به زبان {language} و با لحن دوستانه و کوتاه جواب بده.

=== اطلاعات دانشگاه ===
{context}"""


class ChatReply(BaseModel):
    response: str
    cached: bool


class ChatService:
    def __init__(self, db: AsyncSession, redis_client):
        self.retriever = RagRetriever(db)
        self.provider = get_ai_provider()
        self.cache = ChatCache(redis_client)

    async def ask(self, message: str, language: str = "fa") -> ChatReply:
        # 1. Cache check
        cached = await self.cache.get(message, language)
        if cached:
            return ChatReply(response=cached, cached=True)

        # 2. Retrieve relevant knowledge
        chunks = await self.retriever.retrieve(message)
        context = "\n---\n".join(chunks) if chunks else "اطلاعات موجود نیست."
        system = SYSTEM_PROMPT.format(language=language, context=context)

        # 3. Ask LLM
        answer = await self.provider.chat(
            system, [{"role": "user", "content": message}]
        )

        # 4. Cache for 7 days
        await self.cache.set(message, language, answer)

        return ChatReply(response=answer, cached=False)
