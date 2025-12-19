from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


class AppConfig(BaseModel):
    host: str = "0.0.0.0"
    port: int = 8080


class ApiV1Config(BaseModel):
    prefix: str = "/v1"
    upload_prefix: str = "/upload"


class ApiConfig(BaseModel):
    prefix: str = "/api"
    v1: ApiV1Config = ApiV1Config()


class RabbitMQConfig(BaseModel):
    host: str = "localhost"
    port: int = 5672
    user: str = "guest"
    password: str = "guest"
    virtual_host: str = "/"
    
    @property
    def url(self) -> str:
        return f"amqp://{self.user}:{self.password}@{self.host}:{self.port}/{self.virtual_host}"


class QueueConfig(BaseModel):
    image_queue: str = "image_upload_queue"
    vector_queue: str = "vector_upload_queue"
    exchange: str = "image_exchange"
    image_routing_key: str = "image.upload"
    vector_routing_key: str = "vector.upload"


class Config(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_nested_delimiter="__",
        env_prefix="CONFIG__",
        case_sensitive=False,
        extra="ignore",
    )
    
    app: AppConfig = AppConfig()
    api: ApiConfig = ApiConfig()
    rabbitmq: RabbitMQConfig = RabbitMQConfig()
    queue: QueueConfig = QueueConfig()


config = Config()

