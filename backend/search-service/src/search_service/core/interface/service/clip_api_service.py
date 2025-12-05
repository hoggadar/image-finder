"""Interface for CLIP API service."""

from abc import ABC, abstractmethod
from typing import List


class ClipApiService(ABC):
    """Interface for interacting with CLIP API service."""

    @abstractmethod
    async def get_text_embedding(self, text: str) -> List[float]:
        """
        Get text embedding from CLIP service.
        
        Args:
            text: Text to embed
            
        Returns:
            List of floats representing the text embedding
        """
        pass

