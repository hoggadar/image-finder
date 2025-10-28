from fastapi import Request
from fastapi.responses import JSONResponse
from auth_service.core.exception.base_exeption import BaseAppException


async def base_app_exception_handler(request: Request, exc: BaseAppException):
    """
    Handler for all application-level exceptions that inherit from BaseAppException.
    Returns a structured JSON response with status code, error details, and exception type.
    """
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "status_code": exc.status_code,
            "detail": exc.message,
            "error": type(exc).__name__,
        },
    )