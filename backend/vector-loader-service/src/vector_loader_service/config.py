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
    vector_queue: str = "vector_upload_queue"
    exchange: str = "image_exchange"
    vector_routing_key: str = "vector.upload"


class QdrantConfig(BaseModel):
    host: str
    port: int = 6333
    collection_name: str = "image_vectors"
    vector_size: int = 512


class ClipServiceConfig(BaseModel):
    host: str = "clip"
    port: int = 8080
    
    @property
    def base_url(self) -> str:
        return f"http://{self.host}:{self.port}"


class Config(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_nested_delimiter="__",
        env_prefix="CONFIG__",
        case_sensitive=False,
    )
    
    rabbitmq: RabbitMQConfig
    queue: QueueConfig = QueueConfig()
    qdrant: QdrantConfig
    clip_service: ClipServiceConfig


config = Config()

