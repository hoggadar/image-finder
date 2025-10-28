import uuid

from abc import abstractmethod
from typing import Optional

from auth_service.core.entity.token_entity import RefreshTokenEntity
from auth_service.core.interface.repository.base_repository import BaseRepository


class TokenRepository(BaseRepository[RefreshTokenEntity, uuid.UUID]):
    @abstractmethod
    async def get_by_value(self, value: str) -> Optional[RefreshTokenEntity]:
        pass
    
    @abstractmethod
    async def get_by_user_id(self, user_id: uuid.UUID) -> Optional[RefreshTokenEntity]:
        pass