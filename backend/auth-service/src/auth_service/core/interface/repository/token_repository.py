import uuid

from abc import abstractmethod
from typing import Optional

from auth_service.core.entity.token_entity import TokenEntity
from auth_service.core.interface.repository.base_repository import BaseRepository


class TokenRepository(BaseRepository[TokenEntity, uuid.UUID]):
    @abstractmethod
    async def get_by_value(self, value: str) -> Optional[TokenEntity]:
        pass
    
    @abstractmethod
    async def get_by_user_id(self, user_id: uuid.UUID) -> Optional[TokenEntity]:
        pass