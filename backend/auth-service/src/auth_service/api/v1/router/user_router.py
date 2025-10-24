import logging
import json

from fastapi import APIRouter, Depends, status, HTTPException
from typing import Sequence

from auth_service.api.dependency import get_user_service
from auth_service.api.v1.schema.user_schema import UserSchema, CreateUserSchema, UpdateUserSchema, ChangePasswordSchema
from auth_service.core.interface.service.user_service import UserService
from auth_service.app.util.converter import Converter


user_router = APIRouter()


@user_router.get("/get-all")
async def get_all(
    offset: int = 0,
    limit: int = 10,
    search: str = "",
    user_service: UserService = Depends(get_user_service),
    status_code=status.HTTP_200_OK
):
    users = await user_service.get_all(offset=offset, limit=limit, search=search)
    return [user for user in users]


@user_router.get("/get-by-id/{id}")
async def get_by_id(
    id: str = "",
    user_service: UserService = Depends(get_user_service),
    response_model=UserSchema,
    status_code=status.HTTP_200_OK
):
    user = await user_service.get_by_id(id)
    return user


@user_router.get("/get-by-email/{email}")
async def get_by_email(
    email: str = "",
    user_service: UserService = Depends(get_user_service),
    response_model=UserSchema,
    status_code=status.HTTP_200_OK
):
    user = await user_service.get_by_email(email)
    return user


@user_router.get("/get-by-username/{username}")
async def get_by_username(
    username: str = "",
    user_service: UserService = Depends(get_user_service),
    response_model=UserSchema,
    status_code=status.HTTP_200_OK
):
    user = await user_service.get_by_username(username)
    return user


@user_router.get("/get-by-fullname/{fullname}")
async def get_by_fullname(
    fullname: str = "",
    offset: int = 0,
    limit: int = 10,
    user_service: UserService = Depends(get_user_service),
    status_code=status.HTTP_200_OK
):
    users = await user_service.get_by_fullname(fullname, offset=offset, limit=limit)
    return [user for user in users]


@user_router.post("/create")
async def create(
    dto: CreateUserSchema=None,
    user_service: UserService = Depends(get_user_service),
    response_model=UserSchema,
    status_code=status.HTTP_201_CREATED,
):
    created_user = await user_service.create(dto)
    return created_user


@user_router.patch("/update")
async def update(
    dto: UpdateUserSchema=None,
    user_service: UserService = Depends(get_user_service),
    response_model=UserSchema,
    status_code=status.HTTP_200_OK,
):
    updated_user = await user_service.update(dto)
    return updated_user


@user_router.delete("/delete/{id}")
async def delete(
    id: str = "",
    user_service: UserService = Depends(get_user_service),
    response_model=UserSchema,
    status_code=status.HTTP_200_OK
):
    deleted_user = await user_service.delete(id)
    return deleted_user

