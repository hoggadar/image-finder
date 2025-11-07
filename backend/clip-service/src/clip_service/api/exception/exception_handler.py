from fastapi import Request
from fastapi.responses import JSONResponse

from clip_service.core.exception import BaseAppException


async def exception_handler(request: Request, exc: BaseAppException):
    payload = {
        "status_code": exc.status_code,
        "detail": exc.message,
        "error": type(exc).__name__,
    }

    if exc.details:
        payload["details"] = exc.details

    return JSONResponse(status_code=exc.status_code, content=payload)
