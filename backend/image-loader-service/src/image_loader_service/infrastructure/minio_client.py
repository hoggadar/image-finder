import logging
from io import BytesIO
from uuid import uuid4

from minio import Minio
from minio.error import S3Error

from image_loader_service.config import config

logger = logging.getLogger(__name__)


class MinIOClient:
    def __init__(self):
        self.client: Minio = Minio(
            endpoint=config.minio.endpoint,
            access_key=config.minio.access_key,
            secret_key=config.minio.secret_key,
            secure=config.minio.secure,
            region=config.minio.region,
        )
        self._ensure_bucket_exists()

    def _ensure_bucket_exists(self) -> None:
        try:
            found = self.client.bucket_exists(bucket_name=config.minio.bucket_name)
            if not found:
                self.client.make_bucket(bucket_name=config.minio.bucket_name)
        except S3Error as e:
            logger.error(f"Error ensuring bucket exists: {e}")
            raise

    def upload_image(self, image_data: bytes, filename: str, user_id: str, object_name: str | None = None) -> str:
        if not user_id:
            raise ValueError("user_id is required")
        
        if not object_name:
            if "." in filename:
                file_name_without_ext = ".".join(filename.split(".")[:-1])
                file_extension = filename.split(".")[-1]
            else:
                file_name_without_ext = filename
                file_extension = "jpg"
            
            unique_id = uuid4()
            object_name = f"{user_id}/{file_name_without_ext}_{unique_id}.{file_extension}"
        
        file_extension = object_name.split(".")[-1] if "." in object_name else "jpg"
        
        try:
            image_stream = BytesIO(image_data)
            self.client.put_object(
                bucket_name=config.minio.bucket_name,
                object_name=object_name,
                data=image_stream,
                length=len(image_data),
                content_type=f"image/{file_extension}",
            )
            return object_name
        except S3Error as e:
            logger.error(f"Error uploading image to MinIO: {e}")
            raise


minio_client = MinIOClient()

