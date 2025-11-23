from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


class AppConfig(BaseModel):
    host: str = "0.0.0.0"
    port: int = 8080


class ApiV1Config(BaseModel):
    prefix: str = "/v1"


class ApiConfig(BaseModel):
    prefix: str = "/api"
    v1: ApiV1Config = ApiV1Config()


class RabbitMQConfig(BaseModel):
    host: str
    port: int = 5672
    user: str = "guest"
    password: str = "guest"
    virtual_host: str = "/"
    
    @property
    def url(self) -> str:
        return f"amqp://{self.user}:{self.password}@{self.host}:{self.port}/{self.virtual_host}"


class QueueConfig(BaseModel):
    image_queue: str = "image_upload_queue"
    exchange: str = "image_exchange"
    routing_key: str = "image.upload"


class Config(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_nested_delimiter="__",
        env_prefix="CONFIG__",
        case_sensitive=False,
    )
    
    app: AppConfig = AppConfig()
    api: ApiConfig = ApiConfig()
    rabbitmq: RabbitMQConfig
    queue: QueueConfig = QueueConfig()


config = Config()

