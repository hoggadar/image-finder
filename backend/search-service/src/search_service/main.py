"""Main application entry point."""

from contextlib import asynccontextmanager

from fastapi import FastAPI
import uvicorn
import logging

from search_service.api.api import router
from search_service.api.exception.exception_handler import exception_handler
from search_service.config import config
from search_service.core.exception import BaseAppException
from search_service.logger import setup_logger

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events."""
    logger.info("Search Service starting up...")
    yield
    logger.info("Search Service shutting down...")


def create_app() -> FastAPI:
    setup_logger()

    app = FastAPI(
        title="Search Service",
        description="Image search service using CLIP embeddings and Qdrant",
        version="0.1.0",
        lifespan=lifespan,
    )
    app.add_exception_handler(BaseAppException, exception_handler)
    app.include_router(router)
    
    return app


app = create_app()


if __name__ == "__main__":
    uvicorn.run(app, host=config.app.host, port=config.app.port)

