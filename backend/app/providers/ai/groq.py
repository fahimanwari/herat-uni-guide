import httpx
from app.config import settings
from .base import AIProvider


class GroqProvider(AIProvider):
    """Groq — سازگار با فورمت OpenAI؛ بسیار سریع، سطح رایگان دارد"""

    async def chat(self, system: str, messages: list[dict], max_tokens: int = 800) -> str:
        async with httpx.AsyncClient(timeout=60) as client:
            r = await client.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers={"Authorization": f"Bearer {settings.ai_api_key}"},
                json={
                    "model": settings.ai_model,
                    "max_tokens": max_tokens,
                    "messages": [{"role": "system", "content": system}, *messages],
                },
            )
            r.raise_for_status()
            return r.json()["choices"][0]["message"]["content"]
