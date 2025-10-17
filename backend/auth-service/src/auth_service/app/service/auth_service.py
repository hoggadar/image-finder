import uuid

from abc import ABC, abstractmethod

from auth_service.config import config
from auth_service.core.interface.service.auth_service import AuthService
from auth_service.core.dto.token_dto import TokenPayload


class AuthServiceImpl(AuthService):
    def generate_access_token(self, payload: TokenPayload) -> str:
        expires = config.jwt.access_expire_minutes
        print(expires)
    
    def generate_refresh_token(self) -> str:
        pass
    
    def is_token_expired(self, token_value: str) -> bool:
        pass
    
    def is_token_valid(self, token_value: str) -> bool:
        pass
    
    