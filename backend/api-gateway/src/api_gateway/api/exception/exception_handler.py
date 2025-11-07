from fastapi import Request
from fastapi.responses import JSONResponse

from api_gateway.app.exception import DownstreamServiceException


async def downstream_service_exception_handler(
    request: Request, exc: DownstreamServiceException
) -> JSONResponse:
    payload = exc.payload or {"detail": "Downstream service error"}
    return JSONResponse(status_code=exc.status_code, content=payload)


__all__ = ["downstream_service_exception_handler"]

