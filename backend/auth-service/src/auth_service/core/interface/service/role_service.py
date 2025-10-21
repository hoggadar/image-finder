import uuid

from abc import ABC, abstractmethod
from typing import Sequence, Optional

from auth_service.api.v1.schema.role_schema import RoleSchema, CreateRoleSchema, UpdateRoleSchema

class RoleService(ABC):
    @abstractmethod
    async def get_all(self, offset: int = 0, limit: int = 10, search: str = "") -> Sequence[RoleSchema]:
        pass
    
    @abstractmethod
    async def get_by_id(self, id: uuid.UUID) -> Optional[RoleSchema]:
        pass
    
    @abstractmethod
    async def get_by_name(self, name: str) -> Optional[RoleSchema]:
        pass
    
    @abstractmethod
    async def create(self, dto: CreateRoleSchema) -> Optional[RoleSchema]:
        pass
    
    @abstractmethod
    async def update(self, dto: UpdateRoleSchema) -> Optional[RoleSchema]:
        pass
    
    @abstractmethod
    async def delete(self, id: uuid.UUID) -> Optional[RoleSchema]:
        pass