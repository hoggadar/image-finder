from __future__ import annotations

import asyncio
import logging
from typing import Any, Mapping, MutableMapping, Optional

import httpx

from vector_loader_service.core.interface.service.base_api_service import BaseApiService


logger = logging.getLogger(__name__)


class BaseApiServiceImpl(BaseApiService):
    def __init__(
        self, 
        base_url: str, 
        *, 
        timeout: float = 30.0,
        max_retries: int = 3,
        retry_delay: float = 2.0,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.max_retries = max_retries
        self.retry_delay = retry_delay

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

        last_exception = None
        for attempt in range(self.max_retries):
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
                break
            except (httpx.ConnectError, httpx.TimeoutException) as exc:
                last_exception = exc
                if attempt < self.max_retries - 1:
                    delay = self.retry_delay * (2 ** attempt)
                    logger.warning(
                        f"Connection failed (attempt {attempt + 1}/{self.max_retries}), retrying in {delay}s",
                        extra={"url": url, "error": str(exc)}
                    )
                    await asyncio.sleep(delay)
                else:
                    logger.error(
                        "Failed to reach downstream service after all retries",
                        extra={
                            "url": url,
                            "error": str(exc),
                            "attempts": self.max_retries,
                        }
                    )
                    raise RuntimeError(f"Failed to reach service at {url} after {self.max_retries} attempts: {exc}") from exc
            except httpx.RequestError as exc:
                logger.exception(
                    "Failed to reach downstream service",
                    extra={
                        "url": url,
                        "error": str(exc),
                    }
                )
                raise RuntimeError(f"Failed to reach service at {url}: {exc}") from exc

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
            raise RuntimeError(
                f"Service returned error {response.status_code}: {payload}"
            )

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

