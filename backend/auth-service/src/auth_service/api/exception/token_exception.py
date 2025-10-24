from auth_service.api.exception.base_exception import BaseServiceError


class TokenNotFoundError(BaseServiceError):
    def __init__(self, token_value: str | None = None):
        msg = f"Token '{token_value}' not found" if token_value else "Token not found"
        super().__init__(msg)

class TokenExpiredError(BaseServiceError):
    def __init__(self, token_value: str | None = None):
        msg = f"Token '{token_value}' has expired" if token_value else "Token has expired"

class TokenAlreadyExistsError(BaseServiceError):
    def __init__(self, token_value: str):
        super().__init__(f"Token '{token_value}' already exists")