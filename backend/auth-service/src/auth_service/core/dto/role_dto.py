import uuid

from dataclasses import dataclass


@dataclass
class RoleDTOBase:
    name: str
    description: str


@dataclass
class RoleDTO(RoleDTOBase):
    id: uuid.UUID
    created_at: str
    updated_at: str


@dataclass
class CreateRoleDTO(RoleDTOBase):
    pass


@dataclass
class UpdateRoleDTO(RoleDTOBase):
    id: uuid.UUID