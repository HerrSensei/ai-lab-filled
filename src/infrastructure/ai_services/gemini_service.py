from typing import Any

import google.generativeai as genai

from src.core.config import settings
from src.core.ports.ai_service import IAIService


class GeminiService(IAIService):
    """
    Concrete implementation of IAIService for Google Gemini.
    """

    def __init__(self):
        genai.configure(
            api_key=settings.GEMINI_API_KEY
        )  # Assuming GEMINI_API_KEY in settings

    async def chat_completion(
        self,
        messages: list[dict[str, str]],
        model: str,
        temperature: float,
        max_tokens: int,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """
        Performs a chat completion using Google Gemini's chat models.
        """
        try:
            # Gemini API expects messages in a slightly different format
            # Convert messages from OpenAI format to Gemini format
            gemini_messages = []
            for msg in messages:
                role = "user" if msg["role"] == "user" else "model"
                gemini_messages.append({"role": role, "parts": [msg["content"]]})

            model_instance = genai.GenerativeModel(model)
            response = await model_instance.generate_content_async(
                gemini_messages,
                generation_config=genai.GenerationConfig(
                    temperature=temperature, max_output_tokens=max_tokens, **kwargs
                ),
            )

            # Extract text and estimate token usage (Gemini API doesn't directly provide total_tokens in response)
            generated_text = response.text
            # This is a rough estimate, actual token counting would require a separate call or library
            prompt_tokens = len(
                " ".join([m["parts"][0] for m in gemini_messages]).split()
            )
            completion_tokens = len(generated_text.split())
            total_tokens = prompt_tokens + completion_tokens

            return {
                "text": generated_text,
                "model": model,  # Gemini API response doesn't return model name directly
                "tokens_used": total_tokens,
                "prompt_tokens": prompt_tokens,
                "completion_tokens": completion_tokens,
            }
        except Exception as e:
            raise RuntimeError(f"An unexpected error occurred with Gemini: {e}") from e

    async def generate_text(
        self,
        prompt: str,
        model: str,
        temperature: float,
        max_tokens: int,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """
        Generates text based on a given prompt using Google Gemini's models.
        """
        messages = [{"role": "user", "parts": [prompt]}]
        try:
            model_instance = genai.GenerativeModel(model)
            response = await model_instance.generate_content_async(
                messages,
                generation_config=genai.GenerationConfig(
                    temperature=temperature, max_output_tokens=max_tokens, **kwargs
                ),
            )

            generated_text = response.text
            prompt_tokens = len(prompt.split())
            completion_tokens = len(generated_text.split())
            total_tokens = prompt_tokens + completion_tokens

            return {
                "text": generated_text,
                "model": model,
                "tokens_used": total_tokens,
                "prompt_tokens": prompt_tokens,
                "completion_tokens": completion_tokens,
            }
        except Exception as e:
            raise RuntimeError(f"An unexpected error occurred with Gemini: {e}") from e

    async def get_available_models(self) -> list[str]:
        """
        Retrieves a list of available Google Gemini models.
        """
        # For simplicity, returning a hardcoded list of common models.
        # In a real application, you might call genai.list_models()
        # and filter for generative models.
        return ["gemini-pro", "gemini-pro-vision"]
