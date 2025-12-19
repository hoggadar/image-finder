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
    @abstractmethod
    async def signup(self, payload: SignupSchema) -> TokenPairSchema:
        pass

    @abstractmethod
    async def login(self, payload: LoginSchema) -> TokenPairSchema:
        pass

    @abstractmethod
    async def validate_token(self, payload: ValidateTokenSchema) -> TokenValidationResponse:
        pass

    @abstractmethod
    async def refresh_tokens(self, payload: RefreshTokenSchema) -> TokenPairSchema:
        pass

    @abstractmethod
    async def logout(self) -> dict:
        pass


