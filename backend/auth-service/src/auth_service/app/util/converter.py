import uuid

from auth_service.api.exception.base_exception import InvalidUUIDError


class Converter:
    @staticmethod
    def get_uuid(value: str):
        try:
            return uuid.UUID(value)
        except ValueError:
            raise InvalidUUIDError(value)