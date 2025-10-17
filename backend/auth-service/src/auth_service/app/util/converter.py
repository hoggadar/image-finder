import uuid


class Converter:
    @staticmethod
    def get_uuid(value: str):
        try:
            return uuid.UUID(value)
        except ValueError:
            return None