import logging
import uuid

from fastapi import APIRouter, Depends, status
from typing import Sequence

from auth_service.api.dependency import get_user_service
from auth_service.api.v1.schema.user_schema import UserSchema, CreateUserSchema, UpdateUserSchema, ChangePasswordSchema
from auth_service.core.interface.service.user_service import UserService
from auth_service.core.dto.user_dto import UserDTO, CreateUserDTO, UpdateUserDTO, ChangePasswordDTO


logger = logging.getLogger(__name__)
user_router = APIRouter()


def _dto_to_schema(dto: UserDTO) -> UserSchema:
    return UserSchema(
        id=str(dto.id),
        first_name=dto.first_name,
        last_name=dto.last_name,
        username=dto.username,
        email=dto.email,
        created_at=dto.created_at,
        updated_at=dto.updated_at,
        role_id=str(dto.role_id)
    )


def _create_schema_to_dto(schema: CreateUserSchema) -> CreateUserDTO:
    return CreateUserDTO(
        first_name=schema.first_name,
        last_name=schema.last_name,
        username=schema.username,
        email=schema.email,
        password=schema.password,
        role=schema.role
    )


def _update_schema_to_dto(schema: UpdateUserSchema) -> UpdateUserDTO:
    return UpdateUserDTO(
        id=uuid.UUID(schema.id),
        first_name=schema.first_name,
        last_name=schema.last_name,
        username=schema.username,
        email=schema.email,
        role=schema.role
    )


def _change_password_schema_to_dto(schema: ChangePasswordSchema) -> ChangePasswordDTO:
    return ChangePasswordDTO(
        id=schema.id,
        old_password=schema.old_password,
        new_password=schema.new_password
    )


@user_router.get("/get-all", status_code=status.HTTP_200_OK, response_model=Sequence[UserSchema])
async def get_all(
    offset: int = 0,
    limit: int = 10,
    search: str = "",
    user_service: UserService = Depends(get_user_service),
):
    users_dto = await user_service.get_all(offset=offset, limit=limit, search=search)
    return [_dto_to_schema(user_dto) for user_dto in users_dto]


@user_router.get("/get-by-id/{id}", status_code=status.HTTP_200_OK, response_model=UserSchema)
async def get_by_id(
    id: str,
    user_service: UserService = Depends(get_user_service),
):
    user_dto = await user_service.get_by_id(id)
    return _dto_to_schema(user_dto)


@user_router.get("/get-by-email/{email}", status_code=status.HTTP_200_OK, response_model=UserSchema)
async def get_by_email(
    email: str,
    user_service: UserService = Depends(get_user_service),
):
    user_dto = await user_service.get_by_email(email)
    return _dto_to_schema(user_dto)


@user_router.get("/get-by-username/{username}", status_code=status.HTTP_200_OK, response_model=UserSchema)
async def get_by_username(
    username: str,
    user_service: UserService = Depends(get_user_service),
):
    user_dto = await user_service.get_by_username(username)
    return _dto_to_schema(user_dto)


@user_router.post("/create", status_code=status.HTTP_201_CREATED, response_model=UserSchema)
async def create(
    dto: CreateUserSchema,
    user_service: UserService = Depends(get_user_service),
):
    create_dto = _create_schema_to_dto(dto)
    created_user_dto = await user_service.create(create_dto)
    return _dto_to_schema(created_user_dto)


@user_router.put("/update", status_code=status.HTTP_200_OK, response_model=UserSchema)
async def update(
    dto: UpdateUserSchema,
    user_service: UserService = Depends(get_user_service),
):
    update_dto = _update_schema_to_dto(dto)
    updated_user_dto = await user_service.update(update_dto)
    return _dto_to_schema(updated_user_dto)


@user_router.delete("/delete/{id}", status_code=status.HTTP_200_OK, response_model=UserSchema)
async def delete(
    id: str,
    user_service: UserService = Depends(get_user_service),
):
    deleted_user_dto = await user_service.delete(id)
    return _dto_to_schema(deleted_user_dto)

