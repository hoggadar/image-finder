from fastapi import APIRouter


token_router = APIRouter()


@token_router.get("/refresh")
async def refresh():
    return {"message": "refresh endpoint"}


