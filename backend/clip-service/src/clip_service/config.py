from pydantic import BaseModel
from pydantic_settings import SettingsConfigDict, BaseSettings


class AppConfig(BaseModel):
    host: str = "0.0.0.0"
    port: int = 8080


class ApiV1Config(BaseModel):
    prefix: str = "/v1"
    clip_prefix: str = "/clip"


class ApiConfig(BaseModel):
    prefix: str = "/api"
    v1: ApiV1Config = ApiV1Config()


class ClipModelConfig(BaseModel):
    model_name: str = "openai/clip-vit-base-patch32"


class Config(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_nested_delimiter="__",
        env_prefix="CONFIG__",
        case_sensitive=False,
    )
    app: AppConfig = AppConfig()
    api: ApiConfig = ApiConfig()
    clip_model: ClipModelConfig = ClipModelConfig()


config = Config()