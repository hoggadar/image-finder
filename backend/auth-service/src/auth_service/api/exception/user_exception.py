from auth_service.api.exception.base_exception import BaseServiceError


class UserNotFoundError(BaseServiceError):
    def __init__(self, identifier: str | None = None):
        msg = f"User '{identifier}' not found" if identifier else "User not found"
        super().__init__(msg, status_code=404)


class UserAlreadyExistsError(BaseServiceError):
    def __init__(self, field: str):
        super().__init__(f"User with this {field} already exists", status_code=409)


class PasswordChangeError(BaseServiceError):
    def __init__(self, reason: str):
        super().__init__(f"Password change failed: {reason}", status_code=400)