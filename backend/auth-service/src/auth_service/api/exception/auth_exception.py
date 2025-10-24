from auth_service.api.exception.base_exception import BaseServiceError

class TokenExpiredError(BaseServiceError):
    def __init__(self):
        super().__init__("Token has expired", status_code=401)


class InvalidTokenError(BaseServiceError):
    def __init__(self):
        super().__init__("Invalid token", status_code=401)


class InvalidTokenTypeError(BaseServiceError):
    def __init__(self, expected_type: str):
        super().__init__(f"Invalid token type, expected {expected_type}", status_code=401)
