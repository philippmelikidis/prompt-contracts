"""OpenAI adapter."""

import time
from typing import Tuple
from openai import OpenAI
from .base import AbstractAdapter


class OpenAIAdapter(AbstractAdapter):
    """Adapter for OpenAI models."""
    
    def __init__(self, model: str, params: dict = None):
        super().__init__(model, params)
        self.client = OpenAI()
    
    def generate(self, prompt: str) -> Tuple[str, int]:
        """
        Generate response using OpenAI API.
        
        Args:
            prompt: The prompt text
        
        Returns:
            (response_text, latency_ms)
        """
        start_time = time.time()
        
        # Default parameters
        temperature = self.params.get('temperature', 0)
        max_tokens = self.params.get('max_tokens', None)
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=temperature,
            max_tokens=max_tokens,
        )
        
        end_time = time.time()
        latency_ms = int((end_time - start_time) * 1000)
        
        response_text = response.choices[0].message.content
        
        return response_text, latency_ms

