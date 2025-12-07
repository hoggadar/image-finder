from __future__ import annotations

from typing import Any, Dict

from api_gateway.app.service.base_api_service import BaseApiServiceImpl
from api_gateway.core.interface.service.search import SearchApiService


class SearchApiServiceImpl(BaseApiServiceImpl, SearchApiService):
    """HTTP client responsible for delegating search requests to the Search microservice."""

    def __init__(
        self, base_url: str, endpoints: Dict[str, str], *, timeout: float = 30.0
    ) -> None:
        super().__init__(base_url=base_url, timeout=timeout)
        self._endpoints = endpoints

    async def search_images(
        self, query: str, limit: int = 20, user_id: str | None = None
    ) -> Dict[str, Any]:
        """Search for images by text description."""
        payload = {
            "query": query,
            "limit": limit,
        }
        if user_id:
            payload["user_id"] = user_id
            
        response = await self.post(
            "/api/v1/search/",  # Note: trailing slash required by FastAPI
            json=payload,
        )
        return response

