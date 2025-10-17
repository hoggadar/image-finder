import uuid

from abc import ABC, abstractmethod

from auth_service.core.dto.token_dto import TokenPayload

class AuthService(ABC):
    @abstractmethod
    def generate_access_token(payload: TokenPayload) -> str:
        pass
    
    @abstractmethod
    def generate_refresh_token() -> str:
        pass
    
    @abstractmethod
    def is_token_expired() -> bool:
        pass
    
    @abstractmethod
    def is_token_valid() -> bool:
        pass
    
    