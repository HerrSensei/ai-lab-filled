from typing import Any

import openai

from src.core.config import settings
from src.core.ports.ai_service import IAIService


class OpenAIService(IAIService):
    """
    Concrete implementation of IAIService for OpenAI.
    """

    def __init__(self):
        self.client = openai.AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

    async def chat_completion(
        self,
        messages: list[dict[str, str]],
        model: str,
        temperature: float,
        max_tokens: int,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """
        Performs a chat completion using OpenAI's chat models.
        """
        try:
            response = await self.client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                **kwargs,
            )
            return {
                "text": response.choices[0].message.content,
                "model": response.model,
                "tokens_used": response.usage.total_tokens,
                "prompt_tokens": response.usage.prompt_tokens,
                "completion_tokens": response.usage.completion_tokens,
            }
        except openai.APIError as e:
            # Handle OpenAI API errors
            raise RuntimeError(f"OpenAI API error: {e}") from e
        except Exception as e:
            raise RuntimeError(f"An unexpected error occurred with OpenAI: {e}") from e

    async def generate_text(
        self,
        prompt: str,
        model: str,
        temperature: float,
        max_tokens: int,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """
        Generates text based on a given prompt using OpenAI's models.
        Note: For chat models, this will wrap the prompt in a user message.
        """
        messages = [{"role": "user", "content": prompt}]
        return await self.chat_completion(
            messages, model, temperature, max_tokens, **kwargs
        )

    async def get_available_models(self) -> list[str]:
        """
        Retrieves a list of available OpenAI models.
        Note: This might be rate-limited or require specific permissions.
        For simplicity, returning a hardcoded list of common models.
        """
        # In a real application, you might call client.models.list()
        # and filter for chat-compatible models.
        return ["gpt-4", "gpt-4o", "gpt-3.5-turbo"]
