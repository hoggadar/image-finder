import uuid

from datetime import datetime
from pydantic import BaseModel
from dataclasses import dataclass


class UserDTOBase(BaseModel):
    first_name: str
    last_name: str
    username: str
    email: str


class UserDTO(UserDTOBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime
    role_id: uuid.UUID


class CreateUserDTO(UserDTOBase):
    password: str
    role: str


class UpdateUserDTO(UserDTOBase):
    id: str
    role: str


class ChangePasswordDTO(BaseModel):
    id: uuid.UUID
    old_password: str
    new_password: str