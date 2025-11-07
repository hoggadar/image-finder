from http import HTTPStatus
from typing import Optional

from clip_service.core.exception import BaseAppException


class ClipServiceException(BaseAppException):
    """Base exception for Clip Service application errors."""

    def __init__(
        self, message: str = "Clip service error", *,
        status_code: HTTPStatus = HTTPStatus.INTERNAL_SERVER_ERROR, details: Optional[dict] = None,
    ) -> None:
        super().__init__(message=message, status_code=int(status_code), details=details)


class InvalidImageException(ClipServiceException):
    def __init__(self, message: str = "Provided file is not a valid image") -> None:
        super().__init__(message=message, status_code=HTTPStatus.BAD_REQUEST)


class ModelInferenceException(ClipServiceException):
    def __init__(self, message: str = "Failed to run model inference") -> None:
        super().__init__(message=message, status_code=HTTPStatus.INTERNAL_SERVER_ERROR)


class EmptyTextException(ClipServiceException):
    def __init__(self, message: str = "Text must be provided for similarity calculation") -> None:
        super().__init__(message=message, status_code=HTTPStatus.UNPROCESSABLE_ENTITY)
