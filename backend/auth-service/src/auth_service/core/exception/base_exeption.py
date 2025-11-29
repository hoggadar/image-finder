class BaseException(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


class BaseAppException(BaseException):
    def __init__(self, message: str, status_code: int):
        super().__init__(message)
        self.status_code = status_code


class BaseDatabaseException(BaseException):
    def __init__(self, message: str, details: dict = None):
        super().__init__(message)
        self.details = details


class InvalidUUIDException(BaseAppException):
    def __init__(self, value: str):
        super().__init__(f"Invalid UUID format: {value}", status_code=400)