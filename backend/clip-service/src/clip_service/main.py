from contextlib import asynccontextmanager
from fastapi import FastAPI
import uvicorn
import logging

from clip_service.api.api import router
from clip_service.api.dependency import start_model_loading, is_model_ready
from clip_service.api.exception.exception_handler import exception_handler
from clip_service.config import config
from clip_service.core.exception import BaseAppException
from clip_service.logger import setup_logger

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting CLIP model loading in background...")
    start_model_loading()
    logger.info("API is ready, model loading in background")
    yield
    logger.info("Application shutdown")


def create_app() -> FastAPI:
    setup_logger()

    app = FastAPI(lifespan=lifespan)
    app.add_exception_handler(BaseAppException, exception_handler)
    app.include_router(router)
    
    return app


app = create_app()


if __name__ == "__main__":
    uvicorn.run(app, host=config.app.host, port=config.app.port)