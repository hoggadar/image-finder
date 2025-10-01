from pydantic import BaseModel
from pydantic_settings import SettingsConfigDict, BaseSettings


class AppConfig(BaseModel):
    host: str = "127.0.0.1"
    port: int = 8080


class ApiV1Config(BaseModel):
    prefix: str = "/v1"
    auth_prefix: str = "/auth"
    token_prefix: str = "/token"
    user_prefix: str = "/user"


class ApiConfig(BaseModel):
    prefix: str = "/api"
    service_prefix: str = "/auth-service"
    v1: ApiV1Config


class DatabaseConfig(BaseModel):
    host: str
    port: int
    database: str
    user: str
    password: str
    echo: bool
    echo_pool: bool
    pool_size: int
    max_overflow: int
    pool_timeout: int
    pool_recycle: int

    @property
    def url(self):
        return f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"


class JwtConfig(BaseModel):
    secret: str
    algorithm: str
    access_expire_minutes: int
    refresh_expire_minutes: int


class Config(BaseSettings):
    model_config = SettingsConfigDict(
        env_file="../.env",
        env_nested_delimiter="__",
        env_prefix="CONFIG__",
        case_sensitive=False,
    )
    app: AppConfig
    api: ApiConfig
    db: DatabaseConfig
    jwt: JwtConfig


config = Config()

# print(config.model_dump())