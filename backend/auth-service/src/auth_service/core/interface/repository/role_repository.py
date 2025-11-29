import uuid

from abc import abstractmethod
from typing import Optional

from auth_service.core.entity.role_entity import RoleEntity
from auth_service.core.interface.repository.base_repository import BaseRepository


class RoleRepository(BaseRepository[RoleEntity, uuid.UUID]):
    @abstractmethod
    async def get_by_name(self, name: str) -> Optional[RoleEntity]:
        pass
    