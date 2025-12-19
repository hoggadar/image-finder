from http import HTTPStatus


class BaseAppException(Exception):
    def __init__(
        self, message: str = "Application error", *,
        status_code: int = HTTPStatus.INTERNAL_SERVER_ERROR, details: dict | None = None,
    ) -> None:
        self.message = message
        self.status_code = status_code
        self.details = details or {}
        super().__init__(message)


class SearchException(BaseAppException):
    def __init__(self, message: str = "Search error") -> None:
        super().__init__(message=message, status_code=HTTPStatus.INTERNAL_SERVER_ERROR)


class EmptyQueryException(BaseAppException):
    def __init__(self, message: str = "Search query cannot be empty") -> None:
        super().__init__(message=message, status_code=HTTPStatus.BAD_REQUEST)

