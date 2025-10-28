import uuid

from dataclasses import dataclass


@dataclass
class UserDTOBase:
    first_name: str
    last_name: str
    username: str
    email: str


@dataclass
class UserDTO(UserDTOBase):
    id: uuid.UUID
    created_at: str
    updated_at: str
    role_id: uuid.UUID


@dataclass
class CreateUserDTO(UserDTOBase):
    password: str
    role: str


@dataclass
class UpdateUserDTO(UserDTOBase):
    id: uuid.UUID
    role: str


@dataclass
class ChangePasswordDTO:
    id: uuid.UUID
    old_password: str
    new_password: str