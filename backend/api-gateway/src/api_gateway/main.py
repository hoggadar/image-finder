from fastapi import FastAPI
import uvicorn

from api_gateway.api.api import router
from api_gateway.api.exception.exception_handler import downstream_service_exception_handler
from api_gateway.app.exception import DownstreamServiceException
from api_gateway.config import config


def create_app() -> FastAPI:
    app = FastAPI()
    app.add_exception_handler(DownstreamServiceException, downstream_service_exception_handler)
    app.include_router(router)
    return app


app = create_app()


if __name__ == "__main__":
    uvicorn.run(app, host=config.app.host, port=config.app.port, reload=False)

