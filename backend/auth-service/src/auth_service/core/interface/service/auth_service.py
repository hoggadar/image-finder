import uuid

from abc import ABC, abstractmethod

from auth_service.api.v1.schema.auth_schema import LoginSchema, SignupSchema
from auth_service.api.v1.schema.token_schema import TokenPairSchema
from auth_service.core.dto.token_dto import TokenPayload

class AuthService(ABC):
    @abstractmethod
    def signup(schema: SignupSchema) -> TokenPairSchema:
        pass
    
    @abstractmethod
    def login(schema: LoginSchema) -> TokenPairSchema:
        pass
    
    @abstractmethod
    def generate_access_token(payload: TokenPayload) -> str:
        pass
    
    @abstractmethod
    def generate_refresh_token() -> str:
        pass
    
    @abstractmethod
    def decode_token(access_token: str) -> TokenPayload:
        pass
    
    @abstractmethod
    def validate_refresh_token(refresh_token: str) -> bool:
        pass
    
    @abstractmethod
    def refresh_access_token(access_token: str, refresh_token: str) -> TokenPayload:
        pass
