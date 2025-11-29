from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Mapping, MutableMapping, Optional


class BaseApiService(ABC):
    """Abstraction for HTTP clients that proxy requests to downstream services."""

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
    ) -> Any:
        """Send an HTTP request to the downstream service and return raw response data."""

    @abstractmethod
    async def get(
        self,
        path: str,
        *,
        params: Optional[Mapping[str, Any]] = None,
        headers: Optional[MutableMapping[str, str]] = None,
        timeout: Optional[float] = None,
    ) -> Any:
        """Perform GET request against downstream service."""

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
        """Perform POST request against downstream service."""

    @abstractmethod
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
        """Perform PUT request against downstream service."""

    @abstractmethod
    async def delete(
        self,
        path: str,
        *,
        params: Optional[Mapping[str, Any]] = None,
        headers: Optional[MutableMapping[str, str]] = None,
        timeout: Optional[float] = None,
    ) -> Any:
        """Perform DELETE request against downstream service."""


