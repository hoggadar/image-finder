import logging
import json

from fastapi import APIRouter, Depends, status, HTTPException
from typing import Sequence

from auth_service.api.dependency import get_user_service
from auth_service.core.dto.user_dto import UserDTO
from auth_service.core.interface.service.user_service import UserService
from auth_service.core.dto.user_dto import CreateUserDTO, UpdateUserDTO
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
    response_model=UserDTO,
    status_code=status.HTTP_200_OK
):
    converted_id = Converter.get_uuid(id)
    if not converted_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid UUID format")
    user = await user_service.get_by_id(converted_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


@user_router.get("/get-by-email/{email}")
async def get_by_email(
    email: str = "",
    user_service: UserService = Depends(get_user_service),
    response_model=UserDTO,
    status_code=status.HTTP_200_OK
):
    user = await user_service.get_by_email(email)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


@user_router.get("/get-by-username/{username}")
async def get_by_username(
    username: str = "",
    user_service: UserService = Depends(get_user_service),
    response_model=UserDTO,
    status_code=status.HTTP_200_OK
):
    user = await user_service.get_by_username(username)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


@user_router.get("/get-by-fullname/{fullname}")
async def get_by_fullname(
    user_service: UserService = Depends(get_user_service),
    fullname: str = "",
    offset: int = 0,
    limit: int = 10,
    status_code=status.HTTP_200_OK
):
    users = await user_service.get_by_fullname(fullname, offset=offset, limit=limit)
    if users.count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Users not found")
    return [user for user in users]


@user_router.post("/create")
async def create(
    dto: CreateUserDTO=None,
    user_service: UserService = Depends(get_user_service),
    response_model=UserDTO,
    status_code=status.HTTP_201_CREATED,
):
    created_user = await user_service.create(dto)
    if not created_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User creation failed")
    return created_user


@user_router.patch("/update")
async def update(
    dto: UpdateUserDTO=None,
    user_service: UserService = Depends(get_user_service),
    response_model=UserDTO,
    status_code=status.HTTP_200_OK,
):
    converted_id = Converter.get_uuid(dto.id)
    if not converted_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid UUID format")
    updated_user = await user_service.update(dto)
    if not updated_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User update failed")
    return updated_user


@user_router.delete("/delete/{id}")
async def delete(
    id: str = "",
    user_service: UserService = Depends(get_user_service),
    response_model=UserDTO,
    status_code=status.HTTP_200_OK
):
    converted_id = Converter.get_uuid(id)
    if not converted_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid UUID format")
    deleted_user = await user_service.delete(Converter.get_uuid(id))
    if not deleted_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return deleted_user

