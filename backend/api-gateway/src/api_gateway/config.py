from typing import List, Optional

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


class EndpointConfig(BaseModel):
    name: str
    method: str
    gateway_path: str
    service_path: str
    summary: Optional[str] = None


class ServiceConfig(BaseModel):
    name: str
    base_url: str
    endpoints: List[EndpointConfig]


class ServicesUrlsConfig(BaseModel):
    auth_service_url: str = "http://auth-service:8080"
    clip_service_url: str = "http://clip-service:8080"
    upload_service_url: str = "http://upload-service:8080"
    search_service_url: str = "http://search-service:8080"


class Config(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_nested_delimiter="__",
        env_prefix="CONFIG__",
        case_sensitive=False,
    )

    app: AppConfig = AppConfig()
    api: ApiConfig = ApiConfig()
    service_urls: ServicesUrlsConfig = ServicesUrlsConfig()

    @property
    def services(self) -> List[ServiceConfig]:
        return [
            ServiceConfig(
                name="clip-service",
                base_url=self.service_urls.clip_service_url,
                endpoints=[
                    EndpointConfig(
                        name="GenerateSimilarityReport",
                        method="POST",
                        gateway_path="/api/v1/clip/similarity",
                        service_path="/api/v1/clip/similarity",
                        summary="Calculate similarity between an image and a text prompt.",
                    ),
                    EndpointConfig(
                        name="GetEmbeddings",
                        method="POST",
                        gateway_path="/api/v1/clip/embeddings",
                        service_path="/api/v1/clip/embeddings",
                        summary="Return embeddings for both image and text inputs.",
                    ),
                    EndpointConfig(
                        name="ComparePrecomputedEmbeddings",
                        method="POST",
                        gateway_path="/api/v1/clip/similarity/embeddings",
                        service_path="/api/v1/clip/similarity/embeddings",
                        summary="Compare similarity between provided image and text embeddings.",
                    ),
                    EndpointConfig(
                        name="CompareTextWithImageVector",
                        method="POST",
                        gateway_path="/api/v1/clip/similarity/text-image-vector",
                        service_path="/api/v1/clip/similarity/text-image-vector",
                        summary="Embed user text and compare against a provided image embedding.",
                    ),
                ],
            ),
            ServiceConfig(
                name="auth-service",
                base_url=self.service_urls.auth_service_url,
                endpoints=[
                    EndpointConfig(
                        name="Signup",
                        method="POST",
                        gateway_path="/api/v1/auth/signup",
                        service_path="/api/v1/auth/signup",
                        summary="Register a new user and issue access and refresh tokens.",
                    ),
                    EndpointConfig(
                        name="Login",
                        method="POST",
                        gateway_path="/api/v1/auth/login",
                        service_path="/api/v1/auth/login",
                        summary="Authenticate user credentials and return token pair.",
                    ),
                    EndpointConfig(
                        name="ValidateToken",
                        method="POST",
                        gateway_path="/api/v1/auth/validate_token",
                        service_path="/api/v1/auth/validate_token",
                        summary="Validate access token and optional role requirements.",
                    ),
                    EndpointConfig(
                        name="RefreshTokens",
                        method="POST",
                        gateway_path="/api/v1/auth/refresh",
                        service_path="/api/v1/auth/refresh",
                        summary="Refresh access token using a valid refresh token.",
                    ),
                    EndpointConfig(
                        name="Logout",
                        method="POST",
                        gateway_path="/api/v1/auth/logout",
                        service_path="/api/v1/auth/logout",
                        summary="Invalidate client session (placeholder implementation).",
                    ),
                    EndpointConfig(
                        name="ListUsers",
                        method="GET",
                        gateway_path="/api/v1/user/get-all",
                        service_path="/api/v1/user/get-all",
                        summary="Retrieve paginated list of users with optional search.",
                    ),
                    EndpointConfig(
                        name="GetUserById",
                        method="GET",
                        gateway_path="/api/v1/user/get-by-id/{id}",
                        service_path="/api/v1/user/get-by-id/{id}",
                        summary="Fetch user by unique identifier.",
                    ),
                    EndpointConfig(
                        name="GetUserByEmail",
                        method="GET",
                        gateway_path="/api/v1/user/get-by-email/{email}",
                        service_path="/api/v1/user/get-by-email/{email}",
                        summary="Fetch user by email address.",
                    ),
                    EndpointConfig(
                        name="GetUserByUsername",
                        method="GET",
                        gateway_path="/api/v1/user/get-by-username/{username}",
                        service_path="/api/v1/user/get-by-username/{username}",
                        summary="Fetch user by username.",
                    ),
                    EndpointConfig(
                        name="CreateUser",
                        method="POST",
                        gateway_path="/api/v1/user/create",
                        service_path="/api/v1/user/create",
                        summary="Create a new user with role assignment.",
                    ),
                    EndpointConfig(
                        name="UpdateUser",
                        method="PUT",
                        gateway_path="/api/v1/user/update",
                        service_path="/api/v1/user/update",
                        summary="Update existing user fields and role assignment.",
                    ),
                    EndpointConfig(
                        name="DeleteUser",
                        method="DELETE",
                        gateway_path="/api/v1/user/delete/{id}",
                        service_path="/api/v1/user/delete/{id}",
                        summary="Delete user by identifier.",
                    ),
                    EndpointConfig(
                        name="ListRoles",
                        method="GET",
                        gateway_path="/api/v1/role/get-all",
                        service_path="/api/v1/role/get-all",
                        summary="Retrieve paginated list of roles.",
                    ),
                    EndpointConfig(
                        name="GetRoleById",
                        method="GET",
                        gateway_path="/api/v1/role/get-by-id/{id}",
                        service_path="/api/v1/role/get-by-id/{id}",
                        summary="Fetch role by identifier.",
                    ),
                    EndpointConfig(
                        name="GetRoleByName",
                        method="GET",
                        gateway_path="/api/v1/role/get-by-name/{name}",
                        service_path="/api/v1/role/get-by-name/{name}",
                        summary="Fetch role by name.",
                    ),
                    EndpointConfig(
                        name="CreateRole",
                        method="POST",
                        gateway_path="/api/v1/role/create",
                        service_path="/api/v1/role/create",
                        summary="Create a new role entry.",
                    ),
                    EndpointConfig(
                        name="UpdateRole",
                        method="PUT",
                        gateway_path="/api/v1/role/update",
                        service_path="/api/v1/role/update",
                        summary="Update existing role information.",
                    ),
                    EndpointConfig(
                        name="DeleteRole",
                        method="DELETE",
                        gateway_path="/api/v1/role/delete/{id}",
                        service_path="/api/v1/role/delete/{id}",
                        summary="Delete role by identifier.",
                    ),
                ],
            ),
            ServiceConfig(
                name="upload-service",
                base_url=self.service_urls.upload_service_url,
                endpoints=[
                    EndpointConfig(
                        name="UploadImage",
                        method="POST",
                        gateway_path="/api/v1/upload",
                        service_path="/api/v1/upload",
                        summary="Upload an image file to storage and send to processing queue.",
                    ),
                ],
            ),
            ServiceConfig(
                name="search-service",
                base_url=self.service_urls.search_service_url,
                endpoints=[
                    EndpointConfig(
                        name="SearchImages",
                        method="POST",
                        gateway_path="/api/v1/search",
                        service_path="/api/v1/search",
                        summary="Search for images by text description using CLIP embeddings.",
                    ),
                ],
            ),
        ]


config = Config()


