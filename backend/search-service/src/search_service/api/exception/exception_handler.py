"""Exception handlers for API."""

import logging

from fastapi import Request
from fastapi.responses import JSONResponse

from search_service.core.exception import BaseAppException

logger = logging.getLogger(__name__)


async def exception_handler(request: Request, exc: BaseAppException) -> JSONResponse:
    """Handle application exceptions and return appropriate JSON response."""
    logger.error(
        f"Exception occurred: {exc.message}",
        extra={
            "path": request.url.path,
            "status_code": exc.status_code,
            "details": exc.details,
        },
        exc_info=True,
    )
    
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "status_code": exc.status_code,
            "detail": exc.message,
            "error": exc.__class__.__name__,
            **exc.details,
        },
    )

