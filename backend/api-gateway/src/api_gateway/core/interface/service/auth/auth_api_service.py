from __future__ import annotations

from abc import ABC, abstractmethod

from api_gateway.api.v1.schema.auth import (
    LoginSchema,
    RefreshTokenSchema,
    SignupSchema,
    TokenPairSchema,
    TokenValidationResponse,
    ValidateTokenSchema,
)

from api_gateway.core.interface.service.base_api_service import BaseApiService


class AuthApiService(BaseApiService, ABC):
    """Abstraction describing gateway operations for the auth microservice."""

    @abstractmethod
    async def signup(self, payload: SignupSchema) -> TokenPairSchema:
        """Register a new user and return issued tokens."""

    @abstractmethod
    async def login(self, payload: LoginSchema) -> TokenPairSchema:
        """Authenticate user credentials and return token pair."""

    @abstractmethod
    async def validate_token(self, payload: ValidateTokenSchema) -> TokenValidationResponse:
        """Validate access token and optional role requirements."""

    @abstractmethod
    async def refresh_tokens(self, payload: RefreshTokenSchema) -> TokenPairSchema:
        """Refresh access token using a valid refresh token."""

    @abstractmethod
    async def logout(self) -> dict:
        """Invalidate a user session (implementation defined by downstream service)."""


