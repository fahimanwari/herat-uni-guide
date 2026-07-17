from fastapi import HTTPException, Request
import redis.asyncio as aioredis

from app.config import settings


class RateLimiter:
    def __init__(self):
        self.redis = None

    async def _get_redis(self):
        if self.redis is None:
            self.redis = aioredis.from_url(settings.redis_url)
        return self.redis

    async def check_rate_limit(self, key: str, limit: int = 20, window: int = 86400):
        """Check rate limit. Raises 429 if exceeded."""
        r = await self._get_redis()
        current = await r.incr(f"ratelimit:{key}")
        if current == 1:
            await r.expire(f"ratelimit:{key}", window)
        if current > limit:
            raise HTTPException(
                status_code=429,
                detail=f"تعداد درخواست‌ها بیش از حد مجاز است ({limit} پیام در روز)"
            )


rate_limiter = RateLimiter()
