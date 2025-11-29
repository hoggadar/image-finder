from contextlib import asynccontextmanager
from fastapi import FastAPI
import uvicorn
import logging

from clip_service.api.api import router
from clip_service.api.dependency import get_clip_service
from clip_service.api.exception.exception_handler import exception_handler
from clip_service.config import config
from clip_service.core.exception import BaseAppException
from clip_service.logger import setup_logger

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Preload CLIP model at startup to avoid delays on first request."""
    logger.info("Loading CLIP model at startup...")
    try:
        _ = get_clip_service()
        logger.info("CLIP model loaded successfully")
    except Exception as e:
        logger.error(f"Failed to load CLIP model: {e}", exc_info=True)
        raise
    yield


def create_app() -> FastAPI:
    setup_logger()

    app = FastAPI(lifespan=lifespan)
    app.add_exception_handler(BaseAppException, exception_handler)
    app.include_router(router)
    
    return app


app = create_app()


if __name__ == "__main__":
    uvicorn.run(app, host=config.app.host, port=config.app.port)