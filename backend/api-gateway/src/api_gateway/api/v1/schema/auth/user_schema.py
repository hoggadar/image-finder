import uuid
from datetime import datetime

from pydantic import BaseModel


class UserSchemaBase(BaseModel):
    first_name: str
    last_name: str
    username: str
    email: str


class UserSchema(UserSchemaBase):
    id: str
    created_at: datetime
    updated_at: datetime
    role_id: str


class CreateUserSchema(UserSchemaBase):
    password: str
    role: str


class UpdateUserSchema(UserSchemaBase):
    id: str
    role: str


class ChangePasswordSchema(BaseModel):
    id: uuid.UUID
    old_password: str
    new_password: str


