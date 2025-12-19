from __future__ import annotations

from typing import Any, Dict

from fastapi import UploadFile

from api_gateway.app.service.base_api_service import BaseApiServiceImpl
from api_gateway.core.interface.service.upload import UploadApiService


class UploadApiServiceImpl(BaseApiServiceImpl, UploadApiService):
    def __init__(
        self, base_url: str, endpoints: Dict[str, str], *, timeout: float = 30.0
    ) -> None:
        super().__init__(base_url=base_url, timeout=timeout)
        self._endpoints = endpoints

    async def upload_image(self, file: UploadFile, user_id: str) -> dict[str, Any]:
        image_data = await file.read()
        files = {"file": (file.filename or "unknown", image_data, file.content_type)}
        data = {"user_id": user_id}

        response = await self.post(
            self._endpoints["UploadImage"],
            data=data,
            files=files,
        )
        return response

