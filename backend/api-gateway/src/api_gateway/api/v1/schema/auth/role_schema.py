import uuid
from datetime import datetime

from pydantic import BaseModel


class RoleSchemaBase(BaseModel):
    name: str
    description: str


class RoleSchema(RoleSchemaBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime


class CreateRoleSchema(RoleSchemaBase):
    pass


class UpdateRoleSchema(RoleSchemaBase):
    id: uuid.UUID


