import logging

from minio import Minio
from minio.error import S3Error

from search_service.config import config

logger = logging.getLogger(__name__)


class MinIOClient:
    def __init__(self):
        logger.info(
            "Initializing MinIO client",
            extra={
                "endpoint": config.minio.endpoint,
                "bucket": config.minio.bucket_name,
            }
        )
        self.client: Minio = Minio(
            endpoint=config.minio.endpoint,
            access_key=config.minio.access_key,
            secret_key=config.minio.secret_key,
            secure=config.minio.secure,
            region=config.minio.region,
        )
        self.bucket_name = config.minio.bucket_name

    def get_image(self, object_name: str) -> tuple[bytes, str]:
        try:
            logger.info(
                "Retrieving image from MinIO",
                extra={
                    "object_name": object_name,
                    "bucket": self.bucket_name,
                }
            )
            
            if "/" in object_name:
                user_dir = object_name.split("/")[0]
                try:
                    objects = list(self.client.list_objects(
                        bucket_name=self.bucket_name,
                        prefix=f"{user_dir}/",
                        recursive=True,
                    ))
                    object_names = [obj.object_name for obj in objects]
                    logger.info(
                        "Objects found in user directory",
                        extra={
                            "user_dir": user_dir,
                            "object_count": len(objects),
                            "object_names": object_names,
                            "requested_object": object_name,
                            "object_exists": object_name in object_names,
                        }
                    )
                    
                    if object_name not in object_names:
                        filename_part = object_name.split("/")[-1].split("_")[0] if "_" in object_name.split("/")[-1] else ""
                        similar_objects = [obj for obj in object_names if filename_part in obj] if filename_part else []
                        logger.warning(
                            "Requested object not found, but similar objects exist",
                            extra={
                                "requested": object_name,
                                "similar_objects": similar_objects[:5],
                            }
                        )
                except Exception as e:
                    logger.warning(f"Could not list objects for debugging: {e}")
            
            response = self.client.get_object(
                bucket_name=self.bucket_name,
                object_name=object_name,
            )
            
            image_data = response.read()
            response.close()
            response.release_conn()
            
            content_type = "image/jpeg"
            if "." in object_name:
                ext = object_name.split(".")[-1].lower()
                content_type_map = {
                    "jpg": "image/jpeg",
                    "jpeg": "image/jpeg",
                    "png": "image/png",
                    "gif": "image/gif",
                    "webp": "image/webp",
                }
                content_type = content_type_map.get(ext, "image/jpeg")
            
            logger.debug(f"Successfully retrieved image: {object_name}, size: {len(image_data)} bytes")
            return image_data, content_type
            
        except S3Error as e:
            logger.error(f"Error retrieving image from MinIO: {e}", extra={"object_name": object_name})
            raise
        except Exception as e:
            logger.error(f"Unexpected error retrieving image: {e}", extra={"object_name": object_name}, exc_info=True)
            raise


minio_client = MinIOClient()

