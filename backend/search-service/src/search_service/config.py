from typing import Dict, List, Optional

from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


class AppConfig(BaseModel):
    """Application configuration."""
    host: str = "0.0.0.0"
    port: int = 8080


class ApiV1Config(BaseModel):
    """API v1 configuration."""
    prefix: str = "/v1"
    search_prefix: str = "/search"


class ApiConfig(BaseModel):
    """API configuration."""
    prefix: str = "/api"
    v1: ApiV1Config = ApiV1Config()


class QdrantConfig(BaseModel):
    """Qdrant vector database configuration."""
    host: str = "localhost"
    port: int = 6333
    collection_name: str = "image_vectors"
    search_limit: int = 20  # Default number of results to return


class EndpointConfig(BaseModel):
    """Single endpoint configuration."""
    name: str
    service_path: str
    summary: Optional[str] = None


class ServiceConfig(BaseModel):
    """External service configuration."""
    name: str
    base_url: str
    endpoints: List[EndpointConfig]


class ServicesUrlsConfig(BaseModel):
    """URLs for external services (can be overridden via .env)."""
    clip_service_url: str = "http://clip-service:8080"


class MinIOConfig(BaseModel):
    """MinIO object storage configuration."""
    endpoint: str = "minio-s3:9000"
    access_key: str = "minioadmin"
    secret_key: str = "minioadmin"
    secure: bool = False
    bucket_name: str = "images"
    region: str = "us-east-1"


class Config(BaseSettings):
    """Main configuration for Search Service."""
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_nested_delimiter="__",
        env_prefix="CONFIG__",
        case_sensitive=False,
        extra="ignore",
    )
    
    app: AppConfig = AppConfig()
    api: ApiConfig = ApiConfig()
    qdrant: QdrantConfig = QdrantConfig()
    service_urls: ServicesUrlsConfig = ServicesUrlsConfig()
    minio: MinIOConfig = MinIOConfig()

    @property
    def services(self) -> List[ServiceConfig]:
        """Generate service configurations dynamically."""
        return [
            ServiceConfig(
                name="clip-service",
                base_url=self.service_urls.clip_service_url,
                endpoints=[
                    EndpointConfig(
                        name="GetTextEmbedding",
                        service_path="/api/v1/clip/text-embedding",
                        summary="Get text embedding from CLIP model",
                    ),
                ],
            ),
        ]

    def get_clip_endpoints(self) -> Dict[str, str]:
        """Get CLIP service endpoints as a dictionary."""
        clip_service = next(
            (s for s in self.services if s.name == "clip-service"), None
        )
        if not clip_service:
            raise RuntimeError("CLIP service configuration not found")
        
        return {endpoint.name: endpoint.service_path for endpoint in clip_service.endpoints}


config = Config()

