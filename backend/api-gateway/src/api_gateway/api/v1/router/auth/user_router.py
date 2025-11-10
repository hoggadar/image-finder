from typing import Sequence

from fastapi import APIRouter, status

from api_gateway.api.v1.schema.auth import (
    ChangePasswordSchema,
    CreateUserSchema,
    UpdateUserSchema,
    UserSchema,
)
from api_gateway.api.dependency import UserApiServiceDep
from api_gateway.api.security import require_roles


user_router = APIRouter()


@user_router.get(
    "/get-all",
    status_code=status.HTTP_200_OK,
    response_model=Sequence[UserSchema],
)
@require_roles("Admin", "Moderator")
async def get_all(
    user_service: UserApiServiceDep,
    offset: int = 0,
    limit: int = 10,
    search: str = "",
) -> Sequence[UserSchema]:
    return await user_service.get_all(offset=offset, limit=limit, search=search)


@user_router.get(
    "/get-by-id/{id}",
    status_code=status.HTTP_200_OK,
    response_model=UserSchema,
)
@require_roles("Admin")
async def get_by_id(user_service: UserApiServiceDep, id: str) -> UserSchema:
    return await user_service.get_by_id(id)


@user_router.get(
    "/get-by-email/{email}",
    status_code=status.HTTP_200_OK,
    response_model=UserSchema,
)
@require_roles("Admin")
async def get_by_email(user_service: UserApiServiceDep, email: str) -> UserSchema:
    return await user_service.get_by_email(email)


@user_router.get(
    "/get-by-username/{username}",
    status_code=status.HTTP_200_OK,
    response_model=UserSchema,
)
@require_roles("Admin")
async def get_by_username(user_service: UserApiServiceDep, username: str) -> UserSchema:
    return await user_service.get_by_username(username)


@user_router.post(
    "/create",
    status_code=status.HTTP_201_CREATED,
    response_model=UserSchema,
)
@require_roles("Admin")
async def create(user_service: UserApiServiceDep, payload: CreateUserSchema) -> UserSchema:
    return await user_service.create(payload)


@user_router.put(
    "/update",
    status_code=status.HTTP_200_OK,
    response_model=UserSchema,
)
@require_roles("Admin")
async def update(user_service: UserApiServiceDep, payload: UpdateUserSchema) -> UserSchema:
    return await user_service.update(payload)


@user_router.delete(
    "/delete/{id}",
    status_code=status.HTTP_200_OK,
    response_model=UserSchema,
)
@require_roles("Admin")
async def delete(user_service: UserApiServiceDep, id: str) -> UserSchema:
    return await user_service.delete(id)


@user_router.post(
    "/change-password",
    status_code=status.HTTP_200_OK,
)
@require_roles("Admin")
async def change_password(
    user_service: UserApiServiceDep,
    payload: ChangePasswordSchema,
) -> None:
    await user_service.change_password(payload)


