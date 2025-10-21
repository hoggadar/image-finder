from fastapi import Request
from fastapi.responses import JSONResponse
from auth_service.api.exception.base_exception import BaseServiceError


async def base_service_error_handler(request: Request, exc: BaseServiceError):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "status_code": exc.status_code,
            "detail": exc.message,
            "error": type(exc).__name__,
        },
    )