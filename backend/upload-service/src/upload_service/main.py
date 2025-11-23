import asyncio
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from upload_service.api.router import router
from upload_service.config import config
from upload_service.infrastructure.rabbitmq import rabbitmq_client
from upload_service.logger import setup_logger


@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_logger()
    await rabbitmq_client.connect()
    yield
    await rabbitmq_client.disconnect()


def create_app() -> FastAPI:
    app = FastAPI(
        title="Upload Service",
        description="Service for uploading images to user gallery",
        lifespan=lifespan,
    )
    app.include_router(router, prefix=config.api.v1.prefix)
    return app


app = create_app()


if __name__ == "__main__":
    uvicorn.run(
        app,
        host=config.app.host,
        port=config.app.port,
        reload=False
    )

