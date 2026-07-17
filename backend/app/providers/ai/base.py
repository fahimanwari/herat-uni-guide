from abc import ABC, abstractmethod


class AIProvider(ABC):
    @abstractmethod
    async def chat(
        self, system: str, messages: list[dict], max_tokens: int = 800
    ) -> str: ...
