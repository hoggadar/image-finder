from __future__ import annotations

from typing import Dict, Sequence

from api_gateway.api.v1.schema.auth import CreateRoleSchema, RoleSchema, UpdateRoleSchema
from api_gateway.core.interface.service.auth import RoleApiService

from ..base_api_service import BaseApiServiceImpl


class RoleApiServiceImpl(BaseApiServiceImpl, RoleApiService):
    def __init__(self, base_url: str, endpoints: Dict[str, str], *, timeout: float = 10.0) -> None:
        super().__init__(base_url=base_url, timeout=timeout)
        self._endpoints = endpoints

    async def get_all(self, *, offset: int, limit: int, search: str) -> Sequence[RoleSchema]:
        response = await self.get(
            self._endpoints["ListRoles"],
            params={"offset": offset, "limit": limit, "search": search},
        )
        return [RoleSchema(**item) for item in response]

    async def get_by_id(self, role_id: str) -> RoleSchema:
        endpoint = self._endpoints["GetRoleById"].format(id=role_id)
        response = await self.get(endpoint)
        return RoleSchema(**response)

    async def get_by_name(self, name: str) -> RoleSchema:
        endpoint = self._endpoints["GetRoleByName"].format(name=name)
        response = await self.get(endpoint)
        return RoleSchema(**response)

    async def create(self, payload: CreateRoleSchema) -> RoleSchema:
        response = await self.post(self._endpoints["CreateRole"], json=payload.model_dump())
        return RoleSchema(**response)

    async def update(self, payload: UpdateRoleSchema) -> RoleSchema:
        response = await self.put(self._endpoints["UpdateRole"], json=payload.model_dump())
        return RoleSchema(**response)

    async def delete(self, role_id: str) -> RoleSchema:
        endpoint = self._endpoints["DeleteRole"].format(id=role_id)
        response = await super().delete(endpoint)
        return RoleSchema(**response)


