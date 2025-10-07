"""Ollama adapter."""

import time
import httpx
from typing import Tuple
from .base import AbstractAdapter


class OllamaAdapter(AbstractAdapter):
    """Adapter for Ollama models."""
    
    def __init__(self, model: str, params: dict = None, base_url: str = "http://localhost:11434"):
        super().__init__(model, params)
        self.base_url = base_url
    
    def generate(self, prompt: str) -> Tuple[str, int]:
        """
        Generate response using Ollama API.
        
        Args:
            prompt: The prompt text
        
        Returns:
            (response_text, latency_ms)
        """
        start_time = time.time()
        
        # Build request payload
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
        }
        
        # Add optional parameters
        if 'temperature' in self.params:
            payload['options'] = payload.get('options', {})
            payload['options']['temperature'] = self.params['temperature']
        
        # Make request
        with httpx.Client(timeout=120.0) as client:
            response = client.post(
                f"{self.base_url}/api/generate",
                json=payload
            )
            response.raise_for_status()
            data = response.json()
        
        end_time = time.time()
        latency_ms = int((end_time - start_time) * 1000)
        
        response_text = data.get('response', '')
        
        return response_text, latency_ms

