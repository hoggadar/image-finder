from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from fastapi import UploadFile

from api_gateway.core.interface.service.base_api_service import BaseApiService


class UploadApiService(BaseApiService, ABC):
    """Abstraction describing gateway operations for the Upload microservice."""

    @abstractmethod
    async def upload_image(self, file: UploadFile, user_id: str) -> dict[str, Any]:
        """Upload an image to the upload service for a specific user."""

