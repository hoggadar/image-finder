from auth_service.core.exception.base_exeption import BaseAppException


class TokenNotFoundException(BaseAppException):
    def __init__(self, token_value: str | None = None):
        msg = f"Token '{token_value}' not found" if token_value else "Token not found"
        super().__init__(msg, status_code=404)


class TokenAlreadyExistsException(BaseAppException):
    def __init__(self, token_value: str):
        super().__init__(f"Token '{token_value}' already exists", status_code=409)


class TokenExpiredException(BaseAppException):
    def __init__(self, token_value: str | None = None):
        msg = f"Token '{token_value}' has expired" if token_value else "Token has expired"
        super().__init__(msg, status_code=401)


class InvalidTokenFormatException(BaseAppException):
    def __init__(self, token_format: str):
        super().__init__(f"Invalid token format: {token_format}", status_code=400)


class InvalidTokenException(BaseAppException):
    def __init__(self, reason: str = "Invalid token"):
        super().__init__(reason, status_code=401)


class InvalidTokenTypeException(BaseAppException):
    def __init__(self, expected_type: str):
        super().__init__(f"Invalid token type, expected {expected_type}", status_code=401)


class TokenCreationException(BaseAppException):
    def __init__(self, reason: str):
        super().__init__(f"Token creation failed: {reason}", status_code=400)


class TokenValidationException(BaseAppException):
    def __init__(self, reason: str):
        super().__init__(f"Token validation failed: {reason}", status_code=401)


class TokenRevocationException(BaseAppException):
    def __init__(self, reason: str):
        super().__init__(f"Token revocation failed: {reason}", status_code=400)


class TokenRefreshException(BaseAppException):
    def __init__(self, reason: str):
        super().__init__(f"Token refresh failed: {reason}", status_code=401)
