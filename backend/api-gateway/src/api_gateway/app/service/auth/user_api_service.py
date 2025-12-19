from __future__ import annotations

from typing import Any, Dict, Sequence

from fastapi import HTTPException, status

from api_gateway.api.v1.schema.auth import (
    ChangePasswordSchema,
    CreateUserSchema,
    UpdateUserSchema,
    UserSchema,
)
from api_gateway.core.interface.service.auth import UserApiService

from ..base_api_service import BaseApiServiceImpl


class UserApiServiceImpl(BaseApiServiceImpl, UserApiService):
    def __init__(self, base_url: str, endpoints: Dict[str, str], *, timeout: float = 10.0) -> None:
        super().__init__(base_url=base_url, timeout=timeout)
        self._endpoints = endpoints

    async def get_all(self, *, offset: int, limit: int, search: str) -> Sequence[UserSchema]:
        response = await self.get(
            self._endpoints["ListUsers"],
            params={"offset": offset, "limit": limit, "search": search},
        )
        return [UserSchema(**item) for item in response]

    async def get_by_id(self, user_id: str) -> UserSchema:
        endpoint = self._endpoints["GetUserById"].format(id=user_id)
        response = await self.get(endpoint)
        return UserSchema(**response)

    async def get_by_email(self, email: str) -> UserSchema:
        endpoint = self._endpoints["GetUserByEmail"].format(email=email)
        response = await self.get(endpoint)
        return UserSchema(**response)

    async def get_by_username(self, username: str) -> UserSchema:
        endpoint = self._endpoints["GetUserByUsername"].format(username=username)
        response = await self.get(endpoint)
        return UserSchema(**response)

    async def create(self, payload: CreateUserSchema) -> UserSchema:
        response = await self.post(self._endpoints["CreateUser"], json=payload.model_dump())
        return UserSchema(**response)

    async def update(self, payload: UpdateUserSchema) -> UserSchema:
        response = await self.put(self._endpoints["UpdateUser"], json=payload.model_dump())
        return UserSchema(**response)

    async def delete(self, user_id: str) -> UserSchema:
        endpoint = self._endpoints["DeleteUser"].format(id=user_id)
        response = await super().delete(endpoint)
        return UserSchema(**response)

    async def change_password(self, payload: ChangePasswordSchema) -> None:
        endpoint = self._endpoints.get("ChangePassword")
        if not endpoint:
            raise HTTPException(
                status_code=status.HTTP_501_NOT_IMPLEMENTED,
                detail="Change password endpoint is not configured",
            )

        await self.post(endpoint, json=self._serialize_change_password(payload))

    @staticmethod
    def _serialize_change_password(payload: ChangePasswordSchema) -> Dict[str, Any]:
        data = payload.model_dump()
        data["id"] = str(data["id"])
        return data


