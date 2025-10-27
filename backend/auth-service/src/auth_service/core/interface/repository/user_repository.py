import uuid

from abc import abstractmethod
from typing import Sequence, Optional

from auth_service.core.entity.user_entity import UserEntity
from auth_service.core.interface.repository.base_repository import BaseRepository

class UserRepository(BaseRepository[UserEntity, uuid.UUID]):
    @abstractmethod
    async def get_by_full_name(self, full_name: str, offset: int = 0, limit: int = 10) -> Sequence[UserEntity]:
        pass
    
    @abstractmethod
    async def get_by_username(self, username: str) -> Optional[UserEntity]:
        pass
    
    @abstractmethod
    async def get_by_email(self, email: str) -> Optional[UserEntity]:
        pass