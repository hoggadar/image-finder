class ApiGatewayException(Exception):
    """Base exception for API gateway application errors."""


class DownstreamServiceException(ApiGatewayException):
    """Raised when a downstream microservice returns an error response."""

    def __init__(self, status_code: int, payload: dict | None = None):
        self.status_code = status_code
        self.payload = payload or {}
        message = self.payload.get("detail") or "Downstream service error"
        super().__init__(message)


__all__ = ["ApiGatewayException", "DownstreamServiceException"]

