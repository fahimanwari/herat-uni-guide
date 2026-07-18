from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

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
        self.db = db
        self.provider = get_ai_provider()
        self.cache = ChatCache(redis_client)
        self.retriever = None
        try:
            from .retriever import RagRetriever
            self.retriever = RagRetriever(db)
        except Exception:
            pass  # RAG not available (sentence_transformers not installed)

    async def ask(self, message: str, language: str = "fa") -> ChatReply:
        # 1. Cache check
        cached = await self.cache.get(message, language)
        if cached:
            return ChatReply(response=cached, cached=True)

        # 2. Retrieve relevant knowledge (optional)
        context = ""
        if self.retriever:
            try:
                chunks = await self.retriever.retrieve(message)
                context = "\n---\n".join(chunks) if chunks else ""
            except Exception:
                context = ""

        if context:
            system = SYSTEM_PROMPT.format(language=language, context=context)
        else:
            system = f"تو دستیار هوشمند پوهنتون هرات هستی. به زبان {language} و با لحن دوستانه جواب بده."

        # 3. Ask LLM
        answer = await self.provider.chat(
            system, [{"role": "user", "content": message}]
        )

        # 4. Cache for 7 days
        await self.cache.set(message, language, answer)

        return ChatReply(response=answer, cached=False)
