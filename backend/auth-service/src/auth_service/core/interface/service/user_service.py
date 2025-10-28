import uuid

from abc import ABC, abstractmethod
from typing import Sequence, Optional

from auth_service.core.dto.user_dto import UserDTO, CreateUserDTO, UpdateUserDTO, ChangePasswordDTO


class UserService(ABC):
    @abstractmethod
    async def get_all(self, offset: int = 0, limit: int = 10, search: str = "") -> Sequence[UserDTO]:
        pass
    
    @abstractmethod
    async def get_by_id(self, id: uuid.UUID) -> Optional[UserDTO]:
        pass
    
    @abstractmethod
    async def get_by_username(self, username: str) -> Optional[UserDTO]:
        pass
    
    @abstractmethod
    async def get_by_email(self, email: str) -> Optional[UserDTO]:
        pass
    
    @abstractmethod
    async def create(self, dto: CreateUserDTO) -> Optional[UserDTO]:
        pass
    
    @abstractmethod
    async def update(self, dto: UpdateUserDTO) -> Optional[UserDTO]:
        pass
    
    @abstractmethod
    async def delete(self, id: str) -> Optional[UserDTO]:
        pass
    
    @abstractmethod
    async def change_password(self, dto: ChangePasswordDTO) -> bool:
        pass