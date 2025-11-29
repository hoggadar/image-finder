from datetime import datetime

from pydantic import BaseModel


class TokenSchemaBase(BaseModel):
    value: str
    expires: int
    is_active: bool
    user_id: str


class TokenSchema(TokenSchemaBase):
    id: str
    created_at: datetime
    updated_at: datetime


class CreateTokenSchema(TokenSchemaBase):
    pass


class UpdateTokenSchema(TokenSchemaBase):
    id: str


class TokenPairSchema(BaseModel):
    access_token: str
    refresh_token: str


class RefreshTokenSchema(BaseModel):
    access_token: str
    refresh_token: str


class ValidateTokenSchema(BaseModel):
    access_token: str
    required_role: str


class TokenValidationResponse(BaseModel):
    is_valid: bool
    user_id: str | None = None
    role: str | None = None
    has_required_role: bool = False
    message: str | None = None


