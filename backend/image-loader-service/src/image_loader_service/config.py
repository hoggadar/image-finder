from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


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


class MinIOConfig(BaseModel):
    endpoint: str
    access_key: str
    secret_key: str
    secure: bool = False
    bucket_name: str = "images"
    region: str = "us-east-1"


class Config(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_nested_delimiter="__",
        env_prefix="CONFIG__",
        case_sensitive=False,
    )
    
    rabbitmq: RabbitMQConfig
    queue: QueueConfig = QueueConfig()
    minio: MinIOConfig


config = Config()

