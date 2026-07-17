import hashlib


class ChatCache:
    TTL = 7 * 24 * 3600  # 7 days

    def __init__(self, redis_client):
        self.redis = redis_client

    def _key(self, message: str, language: str) -> str:
        normalized = " ".join(message.strip().lower().split())
        return f"ai:{language}:{hashlib.sha256(normalized.encode()).hexdigest()}"

    async def get(self, message: str, language: str) -> str | None:
        return await self.redis.get(self._key(message, language))

    async def set(self, message: str, language: str, answer: str):
        await self.redis.set(self._key(message, language), answer, ex=self.TTL)
