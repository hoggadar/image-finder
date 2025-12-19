from typing import Dict, List, Optional

from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


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
    vector_queue: str = "vector_upload_queue"
    exchange: str = "image_exchange"
    vector_routing_key: str = "vector.upload"


class QdrantConfig(BaseModel):
    host: str = "localhost"
    port: int = 6333
    collection_name: str = "image_vectors"
    vector_size: int = 512


class EndpointConfig(BaseModel):
    name: str
    service_path: str
    summary: Optional[str] = None


class ServiceConfig(BaseModel):
    name: str
    base_url: str
    endpoints: List[EndpointConfig]


class ServicesUrlsConfig(BaseModel):
    clip_service_url: str = "http://clip-service:8080"


class Config(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_nested_delimiter="__",
        env_prefix="CONFIG__",
        case_sensitive=False,
        extra="ignore",
    )
    
    rabbitmq: RabbitMQConfig = RabbitMQConfig()
    queue: QueueConfig = QueueConfig()
    qdrant: QdrantConfig = QdrantConfig()
    service_urls: ServicesUrlsConfig = ServicesUrlsConfig()

    @property
    def services(self) -> List[ServiceConfig]:
        return [
            ServiceConfig(
                name="clip-service",
                base_url=self.service_urls.clip_service_url,
                endpoints=[
                    EndpointConfig(
                        name="GetEmbeddings",
                        service_path="/api/v1/clip/embeddings",
                        summary="Get image and text embeddings from CLIP model",
                    ),
                    EndpointConfig(
                        name="GetImageEmbedding",
                        service_path="/api/v1/clip/image-embedding",
                        summary="Get image embedding from CLIP model",
                    ),
                    EndpointConfig(
                        name="CalculateSimilarity",
                        service_path="/api/v1/clip/similarity",
                        summary="Calculate similarity between image and text",
                    ),
                ],
            ),
        ]

    def get_clip_endpoints(self) -> Dict[str, str]:
        clip_service = next(
            (s for s in self.services if s.name == "clip-service"), None
        )
        if not clip_service:
            raise RuntimeError("CLIP service configuration not found")
        
        return {endpoint.name: endpoint.service_path for endpoint in clip_service.endpoints}


config = Config()

