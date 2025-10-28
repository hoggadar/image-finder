import uuid

from dataclasses import dataclass
from datetime import datetime


@dataclass
class TokenPayload:
    user_id: uuid.UUID
    role_name: str



# new dtos

@dataclass
class AccessTokenPayloadDTO:
    user_id: uuid.UUID
    role: str


@dataclass
class TokensPairDTO:
    access_token: str
    refresh_token: str


@dataclass
class ValidateTokenDTO:
    access_token: str
    required_role: str


@dataclass
class TokenValidationResultDTO:
    user_id: uuid.UUID | None
    role: str | None
    is_valid: bool
    has_required_role: bool
    message: str | None


@dataclass
class RefreshTokenDTOBase:
    value: str
    is_locked: bool
    expires_at: datetime
    user_id: uuid.UUID


@dataclass
class RefreshTokenDTO(RefreshTokenDTOBase):
    id: uuid.UUID
    created_at: str
    updated_at: str


@dataclass
class CreateRefreshTokenDTO(RefreshTokenDTOBase):
    pass


@dataclass
class UpdateRefreshTokenDTO(RefreshTokenDTOBase):
    id: uuid.UUID