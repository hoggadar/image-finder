from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from fastapi import UploadFile

from api_gateway.core.interface.service.base_api_service import BaseApiService


class UploadApiService(BaseApiService, ABC):
    @abstractmethod
    async def upload_image(self, file: UploadFile, user_id: str) -> dict[str, Any]:
        pass

