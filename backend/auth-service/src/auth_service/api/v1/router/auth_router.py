from fastapi import APIRouter, Depends, status

from auth_service.api.dependency import get_auth_service
from auth_service.core.interface.service.auth_service import AuthService
from auth_service.api.v1.schema.user_schema import UserSchema
from auth_service.api.v1.schema.auth_schema import SignupSchema, LoginSchema
from auth_service.api.v1.schema.token_schema import TokenPairSchema


auth_router = APIRouter()


@auth_router.post("/signup")
async def signup(
    dto: SignupSchema=None,
    auth_service: AuthService = Depends(get_auth_service),
    respone_model=TokenPairSchema,
    status_code=status.HTTP_200_OK
):
    token_pair = await auth_service.signup(dto)
    return token_pair


@auth_router.get("/login")
async def login():
    return {"message": "login endpoint"}


@auth_router.get("/logout")
async def logout():
    return {"message": "logout endpoint"}

