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

    async def ask(self, message: str, language: str = "fa", mode: str = "general") -> ChatReply:
        # 1. Cache check
        cached = await self.cache.get(message, language, mode)
        if cached:
            return ChatReply(response=cached, cached=True)

        # 2. Retrieve relevant knowledge (optional)
        context = ""
        if self.retriever:
            try:
                if mode == "book":
                    # threshold=0.16: فقط chunk‌های مرتبط ارسال شوند
                    # قانون نیوتن=0.148, فعل ماضی=0.147, هایبریدیزیشن=0.155, پایتخت=0.173, بیت‌کوین=0.197
                    chunks = await self.retriever.retrieve(message, source_types=["book"], threshold=0.16)
                else:
                    chunks = await self.retriever.retrieve(message)
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

        # 3. Ask LLM
        answer = await self.provider.chat(
            system, [{"role": "user", "content": message}]
        )

        # 4. Cache for 7 days
        await self.cache.set(message, language, answer, mode)

        return ChatReply(response=answer, cached=False)
