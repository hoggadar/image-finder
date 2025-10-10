import uuid

from datetime import datetime
from dataclasses import dataclass
from typing import Optional


@dataclass
class RoleDTOBase:
    name: str
    description: str


@dataclass
class RoleDTO(RoleDTOBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime


@dataclass
class CreateRoleDTO(RoleDTOBase):
    pass


@dataclass
class UpdateRoleDTO(RoleDTOBase):
    id: uuid.UUID