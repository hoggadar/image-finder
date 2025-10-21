from fastapi import APIRouter, Depends, status

from auth_service.api.dependency import get_user_service
from auth_service.core.interface.service.user_service import UserService
from auth_service.api.v1.schema.user_schema import UserSchema
from auth_service.api.v1.schema.auth_schema import SignupSchema, LoginSchema


auth_router = APIRouter()


@auth_router.post("/signup")
async def signup(
    dto: SignupSchema=None,
    user_service: UserService = Depends(get_user_service),
    respone_model=UserSchema,
    status_code=status.HTTP_200_OK
):
    
    return {"message": "signup endpoint"}


@auth_router.get("/login")
async def login():
    return {"message": "login endpoint"}


@auth_router.get("/logout")
async def logout():
    return {"message": "logout endpoint"}

