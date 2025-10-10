import uvicorn
from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from auth_service.api.api import router
from auth_service.config import config
from auth_service.api.dependency import get_role_service
from auth_service.core.interface.service.role_service import RoleService
from auth_service.infrastructure.db.database import database
from auth_service.infrastructure.db.data_seeder import DataSeeder


app = FastAPI()  

app.include_router(router)
  
@app.get("/")  
async def root():  
    return {"message": "Hello World"}  


@app.get("/seed")
async def seed(
    session: AsyncSession = Depends(database.get_session),
    role_service: RoleService = Depends(get_role_service)
):
    data_seeder = DataSeeder(session=session, role_service=role_service)
    await data_seeder.seed_roles()
    return {"message": "ok"}
    


if __name__ == "__main__":  
    uvicorn.run(app, host=config.app.host, port=config.app.port)