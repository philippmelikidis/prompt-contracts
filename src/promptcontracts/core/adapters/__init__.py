"""LLM adapters for different providers."""

from .base import AbstractAdapter, Capability
from .openai_adapter import OpenAIAdapter
from .ollama_adapter import OllamaAdapter

__all__ = ['AbstractAdapter', 'Capability', 'OpenAIAdapter', 'OllamaAdapter']

