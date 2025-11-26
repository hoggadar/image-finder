from __future__ import annotations

from typing import Any, Dict, List

from api_gateway.app.service.base_api_service import BaseApiServiceImpl
from api_gateway.core.interface.service.search import SearchApiService


class SearchApiServiceImpl(BaseApiServiceImpl, SearchApiService):
    """HTTP client responsible for delegating search requests to the Search microservice.
    
    Note: This implementation is prepared for when a dedicated search service is implemented.
    """

    def __init__(
        self, base_url: str, endpoints: Dict[str, str], *, timeout: float = 30.0
    ) -> None:
        super().__init__(base_url=base_url, timeout=timeout)
        self._endpoints = endpoints

    async def search_by_text(
        self, text: str, limit: int = 10
    ) -> List[dict[str, Any]]:
        """Search for images by text description."""
        response = await self.post(
            self._endpoints["SearchByText"],
            json={"text": text, "limit": limit},
        )
        return response if isinstance(response, list) else []

    async def search_by_image_embedding(
        self, embedding: List[float], limit: int = 10
    ) -> List[dict[str, Any]]:
        """Search for similar images by embedding vector."""
        response = await self.post(
            self._endpoints["SearchByEmbedding"],
            json={"embedding": embedding, "limit": limit},
        )
        return response if isinstance(response, list) else []

    async def search_by_image(
        self, image_url: str, limit: int = 10
    ) -> List[dict[str, Any]]:
        """Search for similar images by image URL."""
        response = await self.post(
            self._endpoints["SearchByImage"],
            json={"image_url": image_url, "limit": limit},
        )
        return response if isinstance(response, list) else []

