import httpx

from app.config import settings
from .base import AIProvider


class GeminiProvider(AIProvider):
    async def chat(self, system: str, messages: list[dict], max_tokens: int = 800) -> str:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{settings.ai_model}:generateContent?key={settings.ai_api_key}"

        contents = [{"role": "user", "parts": [{"text": system}]}]
        for msg in messages:
            contents.append({"role": msg["role"], "parts": [{"text": msg["content"]}]})

        async with httpx.AsyncClient(timeout=60) as client:
            r = await client.post(url, json={"contents": contents})
            r.raise_for_status()
            data = r.json()
            return data["candidates"][0]["content"]["parts"][0]["text"]

    async def chat_with_image(self, system: str, image_base64: str, max_tokens: int = 1500) -> str:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{settings.ai_model}:generateContent?key={settings.ai_api_key}"

        contents = [{
            "role": "user",
            "parts": [
                {"text": system},
                {"inline_data": {"mime_type": "image/jpeg", "data": image_base64}},
            ],
        }]

        async with httpx.AsyncClient(timeout=60) as client:
            r = await client.post(url, json={"contents": contents})
            r.raise_for_status()
            data = r.json()
            return data["candidates"][0]["content"]["parts"][0]["text"]
