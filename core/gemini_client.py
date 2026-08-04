"""Обёртка над GroqClient для совместимости"""
import asyncio
from .groq_client import GroqClient


class GeminiClient:
    def __init__(self):
        self.client = GroqClient()

    async def generate_script(self, topic: str, traits: str = "") -> dict:
        return await self.client.generate_script(topic, traits)
