from typing import Any, Optional


class BaseException(Exception):
    def __init__(self, message: str, *, details: Optional[dict[str, Any]] = None) -> None:
        self.message = message
        self.details = details
        super().__init__(message)


class BaseAppException(BaseException):
    def __init__(self, message: str, status_code: int, *, details: Optional[dict[str, Any]] = None) -> None:
        self.status_code = status_code
        super().__init__(message, details=details)