import asyncio
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from .cache import ChatCache
from app.providers.ai.factory import get_ai_provider


SYSTEM_PROMPT = """تو دستیار هوشمند پوهنتون هرات هستی. فقط بر اساس «اطلاعات دانشگاه»
زیر جواب بده. اگر جواب در اطلاعات نبود، صادقانه بگو نمی‌دانی و پیشنهاد کن
با دانشگاه تماس بگیرند. به زبان {language} و با لحن دوستانه و کوتاه جواب بده.

=== اطلاعات دانشگاه ===
{context}"""

BOOK_SYSTEM_PROMPT = """تو معلم کتاب‌های درسی رسمی وزارت معارف افغانستان هستی.
فقط و فقط از «متن کتاب‌ها» که پایین آمده جواب بده — از دانش خودت هیچ چیزی اضافه نکن.
در پایان جواب، منبع را دقیق بنویس: نام کتاب، صنف و صفحه (در سر هر بخش متن آمده).
اگر جواب در متن کتاب‌ها نبود، فقط بنویس:
«پاسخ این سؤال در کتاب‌های درسی موجود نیست.»
به زبان {language} و ساده جواب بده.

=== متن کتاب‌ها ===
{context}"""

# جایگزین‌های املایی رایج در کتاب‌های درسی
SPELLING_ALIASES = {
    "فتوسنتز": ["فوتوسنتز", "نتز"],
    "کلروفیل": ["کلروفیل", "سبزینه"],
    "میتوکندری": ["میتوکندری", "میتوکوندری"],
    "کربوهیدرات": ["کربوهیدرات", "کربو هیدرات"],
    "پروتئین": ["پروتئین", "پروتين"],
}


def expand_query(query: str) -> str:
    """افزودن جایگزین‌های املایی به سوال برای بهبود جستجو"""
    expanded = query
    for word, aliases in SPELLING_ALIASES.items():
        if word in query:
            for alias in aliases:
                if alias != word and alias not in expanded:
                    expanded += f" {alias}"
    return expanded


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

    async def _chat_with_retry(self, system: str, message: str, max_retries: int = 4) -> str:
        """تماس با LLM با retry در صورت rate limit"""
        for attempt in range(max_retries):
            try:
                return await self.provider.chat(
                    system, [{"role": "user", "content": message}]
                )
            except Exception as e:
                if "429" in str(e) and attempt < max_retries - 1:
                    await asyncio.sleep(3 * (2 ** attempt))  # 3s, 6s, 12s
                else:
                    raise

    async def ask(self, message: str, language: str = "fa", mode: str = "general") -> ChatReply:
        # 1. Cache check
        cached = await self.cache.get(message, language, mode)
        if cached:
            return ChatReply(response=cached, cached=True)

        # 2. Retrieve relevant knowledge (optional)
        context = ""
        if self.retriever:
            try:
                # افزودن جایگزین‌های املایی
                search_query = expand_query(message) if mode == "book" else message

                if mode == "book":
                    # threshold=0.18: فقط chunk‌های مرتبط ارسال شوند
                    chunks = await self.retriever.retrieve(search_query, source_types=["book"], threshold=0.18)
                else:
                    chunks = await self.retriever.retrieve(search_query)
                if chunks:
                    context = "\n---\n".join(c[0] for c in chunks)
            except Exception:
                context = ""

        if mode == "book" and not context:
            # در حالت book اگر اطلاعاتی پیدا نشد، بدون LLM پاسخ برگردان
            answer = "پاسخ این سؤال در کتاب‌های درسی موجود نیست. لطفاً سؤال دیگری مطرح کنید یا با دانشگاه تماس بگیرید."
            await self.cache.set(message, language, answer, mode)
            return ChatReply(response=answer, cached=False)

        if context:
            if mode == "book":
                system = BOOK_SYSTEM_PROMPT.format(language=language, context=context)
            else:
                system = SYSTEM_PROMPT.format(language=language, context=context)
        else:
            system = f"تو دستیار هوشمند پوهنتون هرات هستی. به زبان {language} و با لحن دوستانه جواب بده."

        # 3. Ask LLM with retry
        try:
            answer = await self._chat_with_retry(system, message)
        except Exception:
            answer = "پاسخ این سؤال در کتاب‌های درسی موجود نیست. لطفاً بعداً تلاش کنید."

        # 4. Cache for 7 days
        await self.cache.set(message, language, answer, mode)

        return ChatReply(response=answer, cached=False)
