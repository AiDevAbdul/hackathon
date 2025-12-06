import openai
from typing import List, Dict, Any, Optional
from ..config.settings import settings

class OpenAIService:
    def __init__(self):
        openai.api_key = settings.OPENAI_API_KEY

    async def generate_completion(
        self,
        prompt: str,
        model: str = None,
        max_tokens: int = 1000,
        temperature: float = 0.7,
        **kwargs
    ) -> str:
        """Generate a completion using OpenAI API."""
        if not model:
            model = settings.OPENAI_MODEL

        try:
            response = await openai.ChatCompletion.acreate(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=max_tokens,
                temperature=temperature,
                **kwargs
            )
            return response.choices[0].message.content
        except Exception as e:
            raise Exception(f"Error calling OpenAI API: {str(e)}")

    async def generate_embeddings(self, text: str, model: str = "text-embedding-ada-002") -> List[float]:
        """Generate embeddings for the given text."""
        try:
            response = await openai.Embedding.acreate(input=text, model=model)
            return response.data[0].embedding
        except Exception as e:
            raise Exception(f"Error generating embeddings: {str(e)}")

    async def chat_completion(
        self,
        messages: List[Dict[str, str]],
        model: str = None,
        max_tokens: int = 1000,
        temperature: float = 0.7,
        **kwargs
    ) -> str:
        """Generate a chat completion using OpenAI API."""
        if not model:
            model = settings.OPENAI_MODEL

        try:
            response = await openai.ChatCompletion.acreate(
                model=model,
                messages=messages,
                max_tokens=max_tokens,
                temperature=temperature,
                **kwargs
            )
            return response.choices[0].message.content
        except Exception as e:
            raise Exception(f"Error calling OpenAI API: {str(e)}")