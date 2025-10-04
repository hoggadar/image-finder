import uvicorn
from fastapi import FastAPI

from auth_service.src.api.api import router
from auth_service.src.config import config


app = FastAPI()  

app.include_router(router)
  
@app.get("/")  
async def root():  
    return {"message": "Hello World"}  


if __name__ == "__main__":  
    uvicorn.run(app, host=config.app.host, port=config.app.port)