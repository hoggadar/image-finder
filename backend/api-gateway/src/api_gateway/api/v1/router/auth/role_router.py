from typing import Sequence

from fastapi import APIRouter, status

from api_gateway.api.dependency import RoleApiServiceDep
from api_gateway.api.security import require_roles
from api_gateway.api.tags import ApiTags
from api_gateway.api.v1.schema.auth import (
    CreateRoleSchema,
    RoleSchema,
    UpdateRoleSchema,
)


role_router = APIRouter(tags=[ApiTags.AUTH_ROLES])


@role_router.get(
    "/get-all",
    status_code=status.HTTP_200_OK,
    response_model=Sequence[RoleSchema],
)
@require_roles("Admin")
async def get_all(
    role_service: RoleApiServiceDep,
    offset: int = 0,
    limit: int = 10,
    search: str = "",
) -> Sequence[RoleSchema]:
    return await role_service.get_all(offset=offset, limit=limit, search=search)


@role_router.get(
    "/get-by-id/{id}",
    status_code=status.HTTP_200_OK,
    response_model=RoleSchema,
)
@require_roles("Admin")
async def get_by_id(role_service: RoleApiServiceDep, id: str) -> RoleSchema:
    return await role_service.get_by_id(id)


@role_router.get(
    "/get-by-name/{name}",
    status_code=status.HTTP_200_OK,
    response_model=RoleSchema,
)
@require_roles("Admin")
async def get_by_name(role_service: RoleApiServiceDep, name: str) -> RoleSchema:
    return await role_service.get_by_name(name)


@role_router.post(
    "/create",
    status_code=status.HTTP_201_CREATED,
    response_model=RoleSchema,
)
@require_roles("Admin")
async def create(role_service: RoleApiServiceDep, payload: CreateRoleSchema) -> RoleSchema:
    return await role_service.create(payload)


@role_router.put(
    "/update",
    status_code=status.HTTP_200_OK,
    response_model=RoleSchema,
)
@require_roles("Admin")
async def update(role_service: RoleApiServiceDep, payload: UpdateRoleSchema) -> RoleSchema:
    return await role_service.update(payload)


@role_router.delete(
    "/delete/{id}",
    status_code=status.HTTP_200_OK,
    response_model=RoleSchema,
)
@require_roles("Admin")
async def delete(role_service: RoleApiServiceDep, id: str) -> RoleSchema:
    return await role_service.delete(id)


