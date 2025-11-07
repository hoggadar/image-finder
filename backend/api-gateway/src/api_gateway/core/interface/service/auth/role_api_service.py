from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Sequence

from api_gateway.api.v1.schema.auth import CreateRoleSchema, RoleSchema, UpdateRoleSchema
from api_gateway.core.interface.service.base_api_service import BaseApiService


class RoleApiService(BaseApiService, ABC):
    """Abstraction describing gateway operations that proxy role management endpoints."""

    @abstractmethod
    async def get_all(self, *, offset: int, limit: int, search: str) -> Sequence[RoleSchema]:
        """Retrieve paginated list of roles."""

    @abstractmethod
    async def get_by_id(self, role_id: str) -> RoleSchema:
        """Fetch a role by identifier."""

    @abstractmethod
    async def get_by_name(self, name: str) -> RoleSchema:
        """Fetch a role by name."""

    @abstractmethod
    async def create(self, payload: CreateRoleSchema) -> RoleSchema:
        """Create a new role."""

    @abstractmethod
    async def update(self, payload: UpdateRoleSchema) -> RoleSchema:
        """Update an existing role."""

    @abstractmethod
    async def delete(self, role_id: str) -> RoleSchema:
        """Delete a role by identifier."""


