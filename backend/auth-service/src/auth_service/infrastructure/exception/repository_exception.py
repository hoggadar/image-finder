from auth_service.core.exception.base_exeption import BaseDatabaseException


class RetrievalException(BaseDatabaseException):
    def __init__(self, message: str, details: dict = None):
        super().__init__(f"Database retrieval error: {message}", details)


class CreationExeption(BaseDatabaseException):
    def __init__(self, message: str, details: dict = None):
        super().__init__(f"Database creation error: {message}", details)


class UpdateException(BaseDatabaseException):
    def __init__(self, message: str, details: dict = None):
        super().__init__(f"Database update error: {message}", details)


class DeletionException(BaseDatabaseException):
    def __init__(self, message: str, details: dict = None):
        super().__init__(f"Database deletion error: {message}", details)