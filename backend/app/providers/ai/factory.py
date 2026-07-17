from app.config import settings
from .base import AIProvider
from .gemini import GeminiProvider
from .openrouter import OpenRouterProvider


def get_ai_provider() -> AIProvider:
    match settings.ai_provider:
        case "gemini":
            return GeminiProvider()
        case "openrouter":
            return OpenRouterProvider()
        case _:
            raise ValueError(f"AI provider unknown: {settings.ai_provider}")
