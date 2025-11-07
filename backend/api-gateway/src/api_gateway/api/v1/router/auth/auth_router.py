from fastapi import APIRouter, status

from api_gateway.api.v1.schema.auth import (
    LoginSchema,
    SignupSchema,
    TokenPairSchema,
    TokenValidationResponse,
    ValidateTokenSchema,
    RefreshTokenSchema,
)
from api_gateway.api.dependency import AuthApiServiceDep


auth_router = APIRouter()


@auth_router.post(
    "/signup",
    response_model=TokenPairSchema,
    status_code=status.HTTP_201_CREATED,
)
async def signup(
    schema: SignupSchema,
    auth_service: AuthApiServiceDep,
) -> TokenPairSchema:
    return await auth_service.signup(schema)


@auth_router.post(
    "/login",
    response_model=TokenPairSchema,
    status_code=status.HTTP_200_OK,
)
async def login(
    schema: LoginSchema,
    auth_service: AuthApiServiceDep,
) -> TokenPairSchema:
    return await auth_service.login(schema)


@auth_router.post(
    "/validate_token",
    response_model=TokenValidationResponse,
    status_code=status.HTTP_200_OK,
)
async def validate_token(
    schema: ValidateTokenSchema,
    auth_service: AuthApiServiceDep,
) -> TokenValidationResponse:
    return await auth_service.validate_token(schema)


@auth_router.post(
    "/refresh",
    response_model=TokenPairSchema,
    status_code=status.HTTP_200_OK,
)
async def refresh_tokens(
    schema: RefreshTokenSchema,
    auth_service: AuthApiServiceDep,
) -> TokenPairSchema:
    return await auth_service.refresh_tokens(schema)


@auth_router.post(
    "/logout",
    status_code=status.HTTP_200_OK,
)
async def logout(auth_service: AuthApiServiceDep) -> dict:
    return await auth_service.logout()


