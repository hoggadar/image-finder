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
    """Abstraction describing gateway operations that proxy user management endpoints."""

    @abstractmethod
    async def get_all(self, *, offset: int, limit: int, search: str) -> Sequence[UserSchema]:
        """Retrieve paginated list of users with optional search filter."""

    @abstractmethod
    async def get_by_id(self, user_id: str) -> UserSchema:
        """Fetch a single user by identifier."""

    @abstractmethod
    async def get_by_email(self, email: str) -> UserSchema:
        """Fetch a single user by email."""

    @abstractmethod
    async def get_by_username(self, username: str) -> UserSchema:
        """Fetch a single user by username."""

    @abstractmethod
    async def create(self, payload: CreateUserSchema) -> UserSchema:
        """Create a new user record."""

    @abstractmethod
    async def update(self, payload: UpdateUserSchema) -> UserSchema:
        """Update an existing user."""

    @abstractmethod
    async def delete(self, user_id: str) -> UserSchema:
        """Delete a user by identifier."""

    @abstractmethod
    async def change_password(self, payload: ChangePasswordSchema) -> None:
        """Change user password. Implementations may raise if unsupported."""


