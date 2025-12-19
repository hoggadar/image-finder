from fastapi import FastAPI
import uvicorn

from api_gateway.api.api import router
from api_gateway.api.exception.exception_handler import downstream_service_exception_handler
from api_gateway.api.tags import get_tags_metadata
from api_gateway.app.exception import DownstreamServiceException
from api_gateway.config import config
from api_gateway.logger import setup_logger


def create_app() -> FastAPI:
    setup_logger()
    app = FastAPI(
        title="Image Finder API Gateway",
        description="API Gateway for Image Finder microservices architecture.",
        version="1.0.0",
        openapi_tags=get_tags_metadata(),
    )
    app.add_exception_handler(DownstreamServiceException, downstream_service_exception_handler)
    app.include_router(router)
    return app


app = create_app()


if __name__ == "__main__":
    uvicorn.run(app, host=config.app.host, port=config.app.port, reload=False)

