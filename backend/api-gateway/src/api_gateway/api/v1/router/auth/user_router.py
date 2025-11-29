from typing import Sequence

from fastapi import APIRouter, Depends, status

from api_gateway.api.dependency import UserApiServiceDep
from api_gateway.api.security import require_roles
from api_gateway.api.tags import ApiTags
from api_gateway.api.v1.schema.auth import (
    ChangePasswordSchema,
    CreateUserSchema,
    TokenValidationResponse,
    UpdateUserSchema,
    UserSchema,
)


user_router = APIRouter(tags=[ApiTags.AUTH_USERS])


@user_router.get(
    "/get-all",
    status_code=status.HTTP_200_OK,
    response_model=Sequence[UserSchema],
)
async def get_all(
    user_service: UserApiServiceDep,
    token_data: TokenValidationResponse = Depends(require_roles("Admin", "Moderator")),
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
async def get_by_id(
    user_service: UserApiServiceDep,
    id: str,
    token_data: TokenValidationResponse = Depends(require_roles("Admin")),
) -> UserSchema:
    return await user_service.get_by_id(id)


@user_router.get(
    "/get-by-email/{email}",
    status_code=status.HTTP_200_OK,
    response_model=UserSchema,
)
async def get_by_email(
    user_service: UserApiServiceDep,
    email: str,
    token_data: TokenValidationResponse = Depends(require_roles("Admin")),
) -> UserSchema:
    return await user_service.get_by_email(email)


@user_router.get(
    "/get-by-username/{username}",
    status_code=status.HTTP_200_OK,
    response_model=UserSchema,
)
async def get_by_username(
    user_service: UserApiServiceDep,
    username: str,
    token_data: TokenValidationResponse = Depends(require_roles("Admin")),
) -> UserSchema:
    return await user_service.get_by_username(username)


@user_router.post(
    "/create",
    status_code=status.HTTP_201_CREATED,
    response_model=UserSchema,
)
async def create(
    user_service: UserApiServiceDep,
    payload: CreateUserSchema,
    token_data: TokenValidationResponse = Depends(require_roles("Admin")),
) -> UserSchema:
    return await user_service.create(payload)


@user_router.put(
    "/update",
    status_code=status.HTTP_200_OK,
    response_model=UserSchema,
)
async def update(
    user_service: UserApiServiceDep,
    payload: UpdateUserSchema,
    token_data: TokenValidationResponse = Depends(require_roles("Admin")),
) -> UserSchema:
    return await user_service.update(payload)


@user_router.delete(
    "/delete/{id}",
    status_code=status.HTTP_200_OK,
    response_model=UserSchema,
)
async def delete(
    user_service: UserApiServiceDep,
    id: str,
    token_data: TokenValidationResponse = Depends(require_roles("Admin")),
) -> UserSchema:
    return await user_service.delete(id)


@user_router.post(
    "/change-password",
    status_code=status.HTTP_200_OK,
)
async def change_password(
    user_service: UserApiServiceDep,
    payload: ChangePasswordSchema,
    token_data: TokenValidationResponse = Depends(require_roles("Admin")),
) -> None:
    await user_service.change_password(payload)


