import uuid

from abc import ABC, abstractmethod
from typing import Sequence, Optional

from auth_service.api.v1.schema.token_schema import CreateTokenSchema, TokenSchema


class TokenService(ABC):
    @abstractmethod
    async def get_all(self, offset: int = 0, limit: int = 10, search: str = "") -> Sequence[TokenSchema]:
        pass
    
    @abstractmethod
    async def get_by_id(self, id: str) -> Optional[TokenSchema]:
        pass
    
    @abstractmethod
    async def get_by_value(self, value: str) -> Optional[TokenSchema]:
        pass

    @abstractmethod
    async def get_by_user_id(self, user_id: uuid.UUID) -> Optional[TokenSchema]:
        pass

    @abstractmethod
    async def create(self, dto: CreateTokenSchema) -> TokenSchema:
        pass
    
    @abstractmethod
    async def update(self, dto: TokenSchema) -> TokenSchema:
        pass
    
    @abstractmethod
    async def delete(self, id: str) -> TokenSchema:
        pass

    @abstractmethod
    async def deactivate(self, token: str) -> TokenSchema:
        pass