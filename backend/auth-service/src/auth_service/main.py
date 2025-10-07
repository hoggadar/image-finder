import uvicorn
from fastapi import FastAPI

from src.auth_service.api.api import router
from src.auth_service.config import config


app = FastAPI()  

app.include_router(router)
  
@app.get("/")  
async def root():  
    return {"message": "Hello World"}  


if __name__ == "__main__":  
    uvicorn.run(app, host=config.app.host, port=config.app.port)