from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, List

from api_gateway.core.interface.service.base_api_service import BaseApiService


class SearchApiService(BaseApiService, ABC):
    """Abstraction describing gateway operations for the Search microservice.
    
    Note: This service will be used for vector similarity search operations
    when a dedicated search service is implemented.
    """

    @abstractmethod
    async def search_by_text(self, text: str, limit: int = 10) -> List[dict[str, Any]]:
        """Search for images by text description."""

    @abstractmethod
    async def search_by_image_embedding(
        self, embedding: List[float], limit: int = 10
    ) -> List[dict[str, Any]]:
        """Search for similar images by embedding vector."""

    @abstractmethod
    async def search_by_image(
        self, image_url: str, limit: int = 10
    ) -> List[dict[str, Any]]:
        """Search for similar images by image URL."""

