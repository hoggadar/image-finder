from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Mapping, MutableMapping, Optional

import httpx


class BaseApiService(ABC):
    @abstractmethod
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
        pass

    @abstractmethod
    async def get(
        self,
        path: str,
        *,
        params: Optional[Mapping[str, Any]] = None,
        headers: Optional[MutableMapping[str, str]] = None,
        timeout: Optional[float] = None,
    ) -> Any:
        pass

    @abstractmethod
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
        pass
