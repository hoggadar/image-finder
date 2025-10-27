import uuid

from abc import ABC, abstractmethod
from typing import Sequence, Optional

from auth_service.api.v1.schema.user_schema import UserSchema, CreateUserSchema, UpdateUserSchema, ChangePasswordSchema


class UserService(ABC):
    @abstractmethod
    async def get_all(self, offset: int = 0, limit: int = 10, search: str = "") -> Sequence[UserSchema]:
        pass
    
    @abstractmethod
    async def get_by_id(self, id: uuid.UUID) -> Optional[UserSchema]:
        pass
    
    @abstractmethod
    async def get_by_full_name(self, full_name: str, offset: int = 0, limit: int = 10) -> Sequence[UserSchema]:
        pass
    
    @abstractmethod
    async def get_by_username(self, username: str) -> Optional[UserSchema]:
        pass
    
    @abstractmethod
    async def get_by_email(self, email: str) -> Optional[UserSchema]:
        pass
    
    @abstractmethod
    async def create(self, dto: CreateUserSchema) -> Optional[UserSchema]:
        pass
    
    @abstractmethod
    async def update(self, dto: UpdateUserSchema) -> Optional[UserSchema]:
        pass
    
    @abstractmethod
    async def delete(self, id: uuid.UUID) -> Optional[UserSchema]:
        pass
    
    @abstractmethod
    async def change_password(self, dto: ChangePasswordSchema) -> bool:
        pass