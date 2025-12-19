from __future__ import annotations

import logging
from typing import Any, Mapping, MutableMapping, Optional

import httpx
from fastapi import HTTPException, status

from api_gateway.app.exception import DownstreamServiceException
from api_gateway.core.interface.service.base_api_service import BaseApiService


logger = logging.getLogger(__name__)


class BaseApiServiceImpl(BaseApiService):
    def __init__(self, base_url: str, *, timeout: float = 10.0) -> None:
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    async def request(
        self,
        method: str,
        path: str,
        *,
        params: Optional[Mapping[str, Any]] = None,
        headers: Optional[MutableMapping[str, str]] = None,
        json: Any = None,
        data: Any = None,
        files: Any = None,
        timeout: Optional[float] = None,
    ) -> httpx.Response:
        url = self._compose_url(path)
        request_timeout = timeout or self.timeout

        logger.debug(
            "Dispatching request to downstream service",
            extra={
                "method": method,
                "url": url,
                "params": params,
            },
        )

        try:
            async with httpx.AsyncClient(timeout=request_timeout) as client:
                response = await client.request(
                    method=method,
                    url=url,
                    params=params,
                    headers=headers,
                    json=json,
                    data=data,
                    files=files,
                )
        except httpx.RequestError as exc:
            logger.exception("Failed to reach downstream service", exc_info=exc)
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail={"error": "service_unavailable", "message": str(exc)},
            ) from exc

        if response.status_code >= 400:
            payload = self._safe_json(response)
            logger.warning(
                "Downstream service returned error",
                extra={
                    "status_code": response.status_code,
                    "url": url,
                    "payload": payload,
                },
            )
            raise DownstreamServiceException(response.status_code, payload)

        return response

    async def get(
        self,
        path: str,
        *,
        params: Optional[Mapping[str, Any]] = None,
        headers: Optional[MutableMapping[str, str]] = None,
        timeout: Optional[float] = None,
    ) -> Any:
        response = await self.request(
            "GET",
            path,
            params=params,
            headers=headers,
            timeout=timeout,
        )
        return self._safe_json(response)

    async def post(
        self,
        path: str,
        *,
        params: Optional[Mapping[str, Any]] = None,
        headers: Optional[MutableMapping[str, str]] = None,
        json: Any = None,
        data: Any = None,
        files: Any = None,
        timeout: Optional[float] = None,
    ) -> Any:
        response = await self.request(
            "POST",
            path,
            params=params,
            headers=headers,
            json=json,
            data=data,
            files=files,
            timeout=timeout,
        )
        return self._safe_json(response)

    async def put(
        self,
        path: str,
        *,
        params: Optional[Mapping[str, Any]] = None,
        headers: Optional[MutableMapping[str, str]] = None,
        json: Any = None,
        data: Any = None,
        files: Any = None,
        timeout: Optional[float] = None,
    ) -> Any:
        response = await self.request(
            "PUT",
            path,
            params=params,
            headers=headers,
            json=json,
            data=data,
            files=files,
            timeout=timeout,
        )
        return self._safe_json(response)

    async def delete(
        self,
        path: str,
        *,
        params: Optional[Mapping[str, Any]] = None,
        headers: Optional[MutableMapping[str, str]] = None,
        timeout: Optional[float] = None,
    ) -> Any:
        response = await self.request(
            "DELETE",
            path,
            params=params,
            headers=headers,
            timeout=timeout,
        )
        return self._safe_json(response)

    def _compose_url(self, path: str) -> str:
        if not path.startswith("/"):
            path = f"/{path}"
        return f"{self.base_url}{path}"

    @staticmethod
    def _safe_json(response: httpx.Response) -> Any:
        try:
            return response.json()
        except ValueError:
            return {"detail": response.text}


