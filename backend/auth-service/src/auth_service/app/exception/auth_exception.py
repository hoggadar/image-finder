from auth_service.core.exception.base_exeption import BaseAppException


class AuthenticationException(BaseAppException):
    def __init__(self, message: str = "Authentication failed"):
        super().__init__(message, status_code=401)


class AuthorizationException(BaseAppException):
    def __init__(self, message: str = "Access denied"):
        super().__init__(message, status_code=403)


class LoginException(BaseAppException):
    def __init__(self, reason: str):
        super().__init__(f"Login failed: {reason}", status_code=401)


class LogoutException(BaseAppException):
    def __init__(self, reason: str):
        super().__init__(f"Logout failed: {reason}", status_code=400)


class InvalidCredentialsException(BaseAppException):
    def __init__(self):
        super().__init__("Invalid username or password", status_code=401)


class AccountLockedException(BaseAppException):
    def __init__(self, reason: str = "Account is locked"):
        super().__init__(reason, status_code=423)
