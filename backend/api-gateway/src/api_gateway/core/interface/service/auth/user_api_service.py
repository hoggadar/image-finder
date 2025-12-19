from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Sequence

from api_gateway.api.v1.schema.auth import (
    ChangePasswordSchema,
    CreateUserSchema,
    UpdateUserSchema,
    UserSchema,
)
from api_gateway.core.interface.service.base_api_service import BaseApiService


class UserApiService(BaseApiService, ABC):
    @abstractmethod
    async def get_all(self, *, offset: int, limit: int, search: str) -> Sequence[UserSchema]:
        pass

    @abstractmethod
    async def get_by_id(self, user_id: str) -> UserSchema:
        pass

    @abstractmethod
    async def get_by_email(self, email: str) -> UserSchema:
        pass

    @abstractmethod
    async def get_by_username(self, username: str) -> UserSchema:
        pass

    @abstractmethod
    async def create(self, payload: CreateUserSchema) -> UserSchema:
        pass

    @abstractmethod
    async def update(self, payload: UpdateUserSchema) -> UserSchema:
        pass

    @abstractmethod
    async def delete(self, user_id: str) -> UserSchema:
        pass

    @abstractmethod
    async def change_password(self, payload: ChangePasswordSchema) -> None:
        pass


