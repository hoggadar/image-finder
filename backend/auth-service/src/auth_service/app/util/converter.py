import uuid

from auth_service.core.exception.base_exeption import InvalidUUIDException


class Converter:
    @staticmethod
    def get_uuid(value: str):
        try:
            return uuid.UUID(value)
        except ValueError:
            raise InvalidUUIDException(value)