from pydantic import BaseModel
from datetime import datetime


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

