import uuid

from abc import ABC, abstractmethod
from typing import Sequence, Optional

from auth_service.core.dto.token_dto import RefreshTokenDTO, CreateRefreshTokenDTO, UpdateRefreshTokenDTO


class TokenService(ABC):
    @abstractmethod
    async def get_all(self, offset: int = 0, limit: int = 10, search: str = "") -> Sequence[RefreshTokenDTO]:
        pass
    
    @abstractmethod
    async def get_by_id(self, id: str) -> Optional[RefreshTokenDTO]:
        pass
    
    @abstractmethod
    async def get_by_value(self, value: str) -> Optional[RefreshTokenDTO]:
        pass

    @abstractmethod
    async def get_by_user_id(self, user_id: str) -> Optional[RefreshTokenDTO]:
        pass

    @abstractmethod
    async def create(self, dto: CreateRefreshTokenDTO) -> Optional[RefreshTokenDTO]:
        pass
    
    @abstractmethod
    async def update(self, dto: UpdateRefreshTokenDTO) -> Optional[RefreshTokenDTO]:
        pass
    
    @abstractmethod
    async def delete(self, id: str) -> Optional[RefreshTokenDTO]:
        pass

    @abstractmethod
    async def deactivate(self, token_value: str) -> Optional[RefreshTokenDTO]:
        pass