from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List


class ClipApiService(ABC):
    """Interface for CLIP service HTTP client."""

    @abstractmethod
    async def get_image_embedding(self, image_data: bytes, image_filename: str) -> List[float]:
        pass

    @abstractmethod
    async def get_text_embedding(self, text: str) -> List[float]:
        pass

