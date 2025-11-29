from auth_service.core.exception.base_exeption import BaseAppException


class UserNotFoundException(BaseAppException):
    def __init__(self, field: str | None = None, value: str | None = None):
        if field and value:
            msg = f"User with {field}='{value}' not found"
        elif value:
            msg = f"User '{value}' not found"
        else:
            msg = "User not found"
        super().__init__(msg, status_code=404)
        self.field = field
        self.value = value


class UserAlreadyExistsException(BaseAppException):
    def __init__(self, field: str, value: str):
        super().__init__(f"User with {field}='{value}' already exists", status_code=409)
        self.field = field
        self.value = value


class UserCreationException(BaseAppException):
    def __init__(self, reason: str):
        super().__init__(f"User creation error: {reason}", status_code=400)


class UserUpdateException(BaseAppException):
    def __init__(self, reason: str):
        super().__init__(f"User update failed: {reason}", status_code=400)


class UserDeletionException(BaseAppException):
    def __init__(self, reason: str):
        super().__init__(f"User deletion failed: {reason}", status_code=400)


class PasswordChangeException(BaseAppException):
    def __init__(self, reason: str):
        super().__init__(f"Password change failed: {reason}", status_code=400)
