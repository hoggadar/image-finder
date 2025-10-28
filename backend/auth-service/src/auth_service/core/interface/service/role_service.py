import uuid

from abc import ABC, abstractmethod
from typing import Sequence, Optional

from auth_service.core.dto.role_dto import RoleDTO, CreateRoleDTO, UpdateRoleDTO

class RoleService(ABC):
    @abstractmethod
    async def get_all(self, offset: int = 0, limit: int = 10, search: str = "") -> Sequence[RoleDTO]:
        pass
    
    @abstractmethod
    async def get_by_id(self, id: uuid.UUID) -> Optional[RoleDTO]:
        pass
    
    @abstractmethod
    async def get_by_name(self, name: str) -> Optional[RoleDTO]:
        pass
    
    @abstractmethod
    async def create(self, dto: CreateRoleDTO) -> Optional[RoleDTO]:
        pass
    
    @abstractmethod
    async def update(self, dto: UpdateRoleDTO) -> Optional[RoleDTO]:
        pass
    
    @abstractmethod
    async def delete(self, id: uuid.UUID) -> Optional[RoleDTO]:
        pass