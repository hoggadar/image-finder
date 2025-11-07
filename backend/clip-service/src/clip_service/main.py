from fastapi import FastAPI
import uvicorn

from clip_service.api.api import router
from clip_service.api.exception.exception_handler import exception_handler
from clip_service.config import config
from clip_service.core.exception import BaseAppException
from clip_service.logger import setup_logger


def create_app() -> FastAPI:
    setup_logger()

    app = FastAPI()
    app.add_exception_handler(BaseAppException, exception_handler)
    app.include_router(router)
    return app


app = create_app()


if __name__ == "__main__":
    uvicorn.run(app, host=config.app.host, port=config.app.port)