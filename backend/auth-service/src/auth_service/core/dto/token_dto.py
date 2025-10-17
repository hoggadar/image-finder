import uuid

from dataclasses import dataclass


@dataclass
class TokenPayload:
    user_id: uuid.UUID
    user_email: str