from typing import Any, Dict

from api_gateway.api.v1.schema.auth import (
    LoginSchema,
    RefreshTokenSchema,
    SignupSchema,
    TokenPairSchema,
    TokenValidationResponse,
    ValidateTokenSchema,
)
from api_gateway.core.interface.service.auth.auth_api_service import AuthApiService
from api_gateway.app.service.base_api_service import BaseApiServiceImpl


class AuthApiServiceImpl(BaseApiServiceImpl, AuthApiService):
    def __init__(self, base_url: str, endpoints: Dict[str, str], *, timeout: float = 10.0) -> None:
        super().__init__(base_url=base_url, timeout=timeout)
        self._endpoints = endpoints

    async def signup(self, payload: SignupSchema) -> TokenPairSchema:
        response = await self.post(self._endpoints["Signup"], json=payload.model_dump())
        return TokenPairSchema(**response)

    async def login(self, payload: LoginSchema) -> TokenPairSchema:
        response = await self.post(self._endpoints["Login"], json=payload.model_dump())
        return TokenPairSchema(**response)

    async def validate_token(self, payload: ValidateTokenSchema) -> TokenValidationResponse:
        response = await self.post(self._endpoints["ValidateToken"], json=payload.model_dump())
        return TokenValidationResponse(**response)

    async def refresh_tokens(self, payload: RefreshTokenSchema) -> TokenPairSchema:
        response = await self.post(self._endpoints["RefreshTokens"], json=payload.model_dump())
        return TokenPairSchema(**response)

    async def logout(self) -> Dict[str, Any]:
        return await self.post(self._endpoints["Logout"])


