"""Base adapter interface."""

from abc import ABC, abstractmethod
from typing import Tuple, Dict, Any


class AbstractAdapter(ABC):
    """Base class for LLM adapters."""
    
    def __init__(self, model: str, params: Dict[str, Any] = None):
        """
        Initialize adapter.
        
        Args:
            model: Model identifier
            params: Provider-specific parameters
        """
        self.model = model
        self.params = params or {}
    
    @abstractmethod
    def generate(self, prompt: str) -> Tuple[str, int]:
        """
        Generate a response from the LLM.
        
        Args:
            prompt: The prompt text
        
        Returns:
            (response_text, latency_ms)
        """
        pass

