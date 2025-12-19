from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Sequence

from api_gateway.api.v1.schema.auth import CreateRoleSchema, RoleSchema, UpdateRoleSchema
from api_gateway.core.interface.service.base_api_service import BaseApiService


class RoleApiService(BaseApiService, ABC):
    @abstractmethod
    async def get_all(self, *, offset: int, limit: int, search: str) -> Sequence[RoleSchema]:
        pass

    @abstractmethod
    async def get_by_id(self, role_id: str) -> RoleSchema:
        pass

    @abstractmethod
    async def get_by_name(self, name: str) -> RoleSchema:
        pass

    @abstractmethod
    async def create(self, payload: CreateRoleSchema) -> RoleSchema:
        pass

    @abstractmethod
    async def update(self, payload: UpdateRoleSchema) -> RoleSchema:
        pass

    @abstractmethod
    async def delete(self, role_id: str) -> RoleSchema:
        pass


