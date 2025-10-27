import logging

from fastapi import APIRouter, Depends, status
from typing import Sequence

from auth_service.api.dependency import get_user_service
from auth_service.api.v1.schema.user_schema import UserSchema, CreateUserSchema, UpdateUserSchema, ChangePasswordSchema
from auth_service.core.interface.service.user_service import UserService


logger = logging.getLogger(__name__)
user_router = APIRouter()


@user_router.get("/get-all", status_code=status.HTTP_200_OK, response_model=Sequence[UserSchema])
async def get_all(
    offset: int = 0,
    limit: int = 10,
    search: str = "",
    user_service: UserService = Depends(get_user_service),
):
    users = await user_service.get_all(offset=offset, limit=limit, search=search)
    return users


@user_router.get("/get-by-id/{id}", status_code=status.HTTP_200_OK, response_model=UserSchema)
async def get_by_id(
    id: str,
    user_service: UserService = Depends(get_user_service),
):
    user = await user_service.get_by_id(id)
    return user


@user_router.get("/get-by-email/{email}", status_code=status.HTTP_200_OK, response_model=UserSchema)
async def get_by_email(
    email: str,
    user_service: UserService = Depends(get_user_service),
):
    user = await user_service.get_by_email(email)
    return user


@user_router.get("/get-by-username/{username}", status_code=status.HTTP_200_OK, response_model=UserSchema)
async def get_by_username(
    username: str,
    user_service: UserService = Depends(get_user_service),
):
    user = await user_service.get_by_username(username)
    return user


@user_router.get("/get-by-full_name/{full_name}", status_code=status.HTTP_200_OK, response_model=Sequence[UserSchema])
async def get_by_full_name(
    fullname: str,
    offset: int = 0,
    limit: int = 10,
    user_service: UserService = Depends(get_user_service),
):
    users = await user_service.get_by_full_name(fullname, offset=offset, limit=limit)
    return users


@user_router.post("/create", status_code=status.HTTP_201_CREATED, response_model=UserSchema)
async def create(
    dto: CreateUserSchema,
    user_service: UserService = Depends(get_user_service),
):
    created_user = await user_service.create(dto)
    return created_user


@user_router.patch("/update", status_code=status.HTTP_200_OK, response_model=UserSchema)
async def update(
    dto: UpdateUserSchema,
    user_service: UserService = Depends(get_user_service),
):
    updated_user = await user_service.update(dto)
    return updated_user


@user_router.delete("/delete/{id}", status_code=status.HTTP_200_OK, response_model=UserSchema)
async def delete(
    id: str,
    user_service: UserService = Depends(get_user_service),
):
    deleted_user = await user_service.delete(id)
    return deleted_user

