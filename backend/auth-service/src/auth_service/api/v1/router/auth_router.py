from fastapi import APIRouter


auth_router = APIRouter()


@auth_router.get("/signup")
async def signup():
    return {"message": "signup endpoint"}


@auth_router.get("/login")
async def login():
    return {"message": "login endpoint"}


@auth_router.get("/logout")
async def logout():
    return {"message": "logout endpoint"}

