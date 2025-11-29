import uuid
import logging

from fastapi import APIRouter, Depends, status
from typing import Sequence

from auth_service.api.dependency import get_role_service
from auth_service.api.v1.schema.role_schema import RoleSchema, CreateRoleSchema, UpdateRoleSchema
from auth_service.core.interface.service.role_service import RoleService
from auth_service.core.dto.role_dto import RoleDTO, CreateRoleDTO, UpdateRoleDTO


logger = logging.getLogger(__name__)
role_router = APIRouter()


def _dto_to_schema(dto: RoleDTO) -> RoleSchema:
    return RoleSchema(
        id=dto.id,
        name=dto.name,
        description=dto.description,
        created_at=dto.created_at,
        updated_at=dto.updated_at
    )


def _create_schema_to_dto(schema: CreateRoleSchema) -> CreateRoleDTO:
    return CreateRoleDTO(
        name=schema.name,
        description=schema.description
    )


def _update_schema_to_dto(schema: UpdateRoleSchema) -> UpdateRoleDTO:
    return UpdateRoleDTO(
        id=schema.id,
        name=schema.name,
        description=schema.description
    )


@role_router.get("/get-all", status_code=status.HTTP_200_OK, response_model=Sequence[RoleSchema])
async def get_all(
    offset: int = 0,
    limit: int = 10,
    search: str = "",
    role_service: RoleService = Depends(get_role_service),
):
    roles_dto = await role_service.get_all(offset=offset, limit=limit, search=search)
    return [_dto_to_schema(role_dto) for role_dto in roles_dto]


@role_router.get("/get-by-id/{id}", status_code=status.HTTP_200_OK, response_model=RoleSchema)
async def get_by_id(
    id: str,
    role_service: RoleService = Depends(get_role_service),
):
    role_dto = await role_service.get_by_id(uuid.UUID(id))
    return _dto_to_schema(role_dto)


@role_router.get("/get-by-name/{name}", status_code=status.HTTP_200_OK, response_model=RoleSchema)
async def get_by_name(
    name: str,
    role_service: RoleService = Depends(get_role_service),
):
    role_dto = await role_service.get_by_name(name)
    return _dto_to_schema(role_dto)


@role_router.post("/create", status_code=status.HTTP_201_CREATED, response_model=RoleSchema)
async def create(
    dto: CreateRoleSchema,
    role_service: RoleService = Depends(get_role_service),
):
    create_dto = _create_schema_to_dto(dto)
    created_role_dto = await role_service.create(create_dto)
    return _dto_to_schema(created_role_dto)


@role_router.put("/update", status_code=status.HTTP_200_OK, response_model=RoleSchema)
async def update(
    dto: UpdateRoleSchema,
    role_service: RoleService = Depends(get_role_service),
):
    update_dto = _update_schema_to_dto(dto)
    updated_role_dto = await role_service.update(update_dto)
    return _dto_to_schema(updated_role_dto)


@role_router.delete("/delete/{id}", status_code=status.HTTP_200_OK, response_model=RoleSchema)
async def delete(
    id: str,
    role_service: RoleService = Depends(get_role_service),
):
    deleted_role_dto = await role_service.delete(uuid.UUID(id))
    return _dto_to_schema(deleted_role_dto)
