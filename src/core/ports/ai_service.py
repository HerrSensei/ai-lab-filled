from abc import ABC, abstractmethod
from typing import Any


class IAIService(ABC):
    """
    Abstract Base Class for AI Services.

    Defines the interface for various AI provider integrations,
    ensuring provider-agnostic interaction with AI models.
    """

    @abstractmethod
    async def chat_completion(
        self,
        messages: list[dict[str, str]],
        model: str,
        temperature: float,
        max_tokens: int,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """
        Performs a chat completion using the AI model.

        Args:
            messages (List[Dict[str, str]]): A list of message dictionaries,
                                              each with 'role' and 'content'.
            model (str): The name of the AI model to use.
            temperature (float): Controls the randomness of the output.
            max_tokens (int): The maximum number of tokens to generate.
            **kwargs (Any): Additional parameters specific to the AI provider.

        Returns:
            Dict[str, Any]: A dictionary containing the AI model's response,
                            including generated text, token usage, etc.
        """
        pass

    @abstractmethod
    async def generate_text(
        self,
        prompt: str,
        model: str,
        temperature: float,
        max_tokens: int,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """
        Generates text based on a given prompt using the AI model.

        Args:
            prompt (str): The input text prompt.
            model (str): The name of the AI model to use.
            temperature (float): Controls the randomness of the output.
            max_tokens (int): The maximum number of tokens to generate.
            **kwargs (Any): Additional parameters specific to the AI provider.

        Returns:
            Dict[str, Any]: A dictionary containing the AI model's response,
                            including generated text, token usage, etc.
        """
        pass

    @abstractmethod
    async def get_available_models(self) -> list[str]:
        """
        Retrieves a list of available models for the AI service.

        Returns:
            List[str]: A list of model names.
        """
        pass
