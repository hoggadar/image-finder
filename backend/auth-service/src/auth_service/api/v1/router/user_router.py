import logging
import json

from fastapi import APIRouter, Depends
from typing import Sequence

from auth_service.api.dependency import get_user_service
from auth_service.core.dto.user_dto import UserDTO
from auth_service.core.interface.service.user_service import UserService
from auth_service.app.util.converter import Converter


user_router = APIRouter()


@user_router.get("/get-all")
async def get_all(
    user_service: UserService = Depends(get_user_service),
    offset: int = 0,
    limit: int = 10,
    search: str = ""
):
    users = await user_service.get_all(offset=offset, limit=limit, search=search)
    return {"users": [user.__dict__ for user in users]}


@user_router.get("/get-by-id/{id}")
async def get(
    user_service: UserService = Depends(get_user_service),
    id: str = ""
):
    converted_id = Converter.get_uuid(id)
    if not converted_id:
        return {"message": "Invalid UUID format"}
    user = await user_service.get_by_id(converted_id)
    return {"user": user}


@user_router.get("/get-by-username/{username}")



@user_router.get("/create")
async def create():
    return {"message": "create endpoint"}


@user_router.get("/update")
async def update():
    return {"message": "update endpoint"}


@user_router.get("/delete")
async def delete():
    return {"message": "delete endpoint"}

