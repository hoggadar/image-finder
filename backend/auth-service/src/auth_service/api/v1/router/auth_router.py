from fastapi import APIRouter, Depends, status

from auth_service.api.dependency import get_auth_service
from auth_service.core.interface.service.auth_service import AuthService
from auth_service.api.v1.schema.user_schema import UserSchema
from auth_service.api.v1.schema.auth_schema import SignupSchema, LoginSchema
from auth_service.api.v1.schema.token_schema import (
    TokenPairSchema, 
    RefreshTokenSchema,
    ValidateTokenSchema,
    TokenValidationResponse
)
from auth_service.core.dto.auth_dto import LoginDTO, SignupDTO
from auth_service.core.dto.token_dto import TokensPairDTO, TokenValidationResultDTO


auth_router = APIRouter()


def _signup_schema_to_dto(schema: SignupSchema) -> SignupDTO:
    return SignupDTO(
        first_name=schema.first_name,
        last_name=schema.last_name,
        username=schema.username,
        email=schema.email,
        password=schema.password
    )


def _login_schema_to_dto(schema: LoginSchema) -> LoginDTO:
    return LoginDTO(
        email=schema.email,
        password=schema.password
    )


def _tokens_pair_dto_to_schema(dto: TokensPairDTO) -> TokenPairSchema:
    return TokenPairSchema(
        access_token=dto.access_token,
        refresh_token=dto.refresh_token
    )


def _token_validation_result_dto_to_schema(dto: TokenValidationResultDTO) -> TokenValidationResponse:
    return TokenValidationResponse(
        is_valid=dto.is_valid,
        user_id=str(dto.user_id) if dto.user_id else None,
        role=dto.role,
        has_required_role=dto.has_required_role,
        message=dto.message
    )


@auth_router.post(
    "/signup",
    response_model=TokenPairSchema,
    status_code=status.HTTP_201_CREATED
)
async def signup(
    schema: SignupSchema,
    auth_service: AuthService = Depends(get_auth_service),
) -> TokenPairSchema:
    signup_dto = _signup_schema_to_dto(schema)
    tokens_pair_dto = await auth_service.signup(signup_dto)
    return _tokens_pair_dto_to_schema(tokens_pair_dto)


@auth_router.post(
    "/login",
    response_model=TokenPairSchema,
    status_code=status.HTTP_200_OK
)
async def login(
    schema: LoginSchema,
    auth_service: AuthService = Depends(get_auth_service),
) -> TokenPairSchema:
    login_dto = _login_schema_to_dto(schema)
    tokens_pair_dto = await auth_service.login(login_dto)
    return _tokens_pair_dto_to_schema(tokens_pair_dto)


@auth_router.post(
    "/validate_token",
    response_model=TokenValidationResponse,
    status_code=status.HTTP_200_OK
)
async def validate_token(
    schema: ValidateTokenSchema,
    auth_service: AuthService = Depends(get_auth_service),
) -> TokenValidationResponse:
    validation_result_dto = await auth_service.validate_access_token_with_role(
        access_token=schema.access_token,
        required_role=schema.required_role
    )
    return _token_validation_result_dto_to_schema(validation_result_dto)


@auth_router.post(
    "/refresh",
    response_model=TokenPairSchema,
    status_code=status.HTTP_200_OK
)
async def refresh_tokens(
    schema: RefreshTokenSchema,
    auth_service: AuthService = Depends(get_auth_service),
) -> TokenPairSchema:
    tokens_pair_dto = await auth_service.refresh_access_token(
        access_token=schema.access_token,
        refresh_token=schema.refresh_token
    )
    return _tokens_pair_dto_to_schema(tokens_pair_dto)


@auth_router.post("/logout")
async def logout():
    return {"message": "logout endpoint"}

