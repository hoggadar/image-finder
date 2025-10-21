from auth_service.api.exception.base_exception import BaseServiceError
from auth_service.api.exception.exception_handler import base_service_error_handler
import uvicorn
import logging

from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from auth_service.logger import setup_logger
from auth_service.api.api import router
from auth_service.config import config
from auth_service.api.dependency import get_role_service, get_user_service
from auth_service.core.interface.service.role_service import RoleService
from auth_service.core.interface.service.user_service import UserService
from auth_service.infrastructure.db.database import database
from auth_service.infrastructure.db.data_seeder import DataSeeder


setup_logger()

app = FastAPI()
app.add_exception_handler(BaseServiceError, base_service_error_handler)
app.include_router(router)


@app.get("/")  
async def root():  
    return {"message": "Hello World"}  


@app.get("/seed")
async def seed(
    role_service: RoleService = Depends(get_role_service),
    user_service: UserService = Depends(get_user_service)
):
    data_seeder = DataSeeder(role_service=role_service, user_service=user_service)
    await data_seeder.seed_roles()
    await data_seeder.seed_users()
    return {"message": "ok"}


if __name__ == "__main__":  
    uvicorn.run(app, host=config.app.host, port=config.app.port)