from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Dict

from api_gateway.core.interface.service.base_api_service import BaseApiService


class SearchApiService(BaseApiService, ABC):
    """Abstraction describing gateway operations for the Search microservice."""

    @abstractmethod
    async def search_images(
        self, query: str, limit: int = 20, user_id: str | None = None
    ) -> Dict[str, Any]:
        """Search for images by text description using CLIP embeddings."""

