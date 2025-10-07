from fastapi import APIRouter


user_router = APIRouter()


@user_router.get("/get-all")
async def get_all():
    return {"message": "get-all endpoint"}


@user_router.get("/get")
async def get():
    return {"message": "get endpoint"}


@user_router.get("/create")
async def create():
    return {"message": "create endpoint"}


@user_router.get("/update")
async def update():
    return {"message": "update endpoint"}


@user_router.get("/delete")
async def delete():
    return {"message": "delete endpoint"}

