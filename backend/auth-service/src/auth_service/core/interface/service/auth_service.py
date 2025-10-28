import uuid

from abc import ABC, abstractmethod

from auth_service.core.dto.auth_dto import LoginDTO, SignupDTO
from auth_service.core.dto.token_dto import AccessTokenPayloadDTO, TokensPairDTO, TokenValidationResultDTO

class AuthService(ABC):
    @abstractmethod
    def signup(dto: SignupDTO) -> TokensPairDTO:
        pass
    
    @abstractmethod
    def login(dto: LoginDTO) -> TokensPairDTO:
        pass
    
    @abstractmethod
    def generate_access_token(payload: AccessTokenPayloadDTO) -> str:
        pass
    
    @abstractmethod
    def generate_refresh_token() -> str:
        pass
    
    @abstractmethod
    def decode_token(access_token: str) -> AccessTokenPayloadDTO:
        pass
    
    @abstractmethod
    def validate_access_token_with_role(access_token: str, required_role: str) -> TokenValidationResultDTO:
        pass
    
    @abstractmethod
    def refresh_access_token(access_token: str, refresh_token: str) -> TokensPairDTO:
        pass
