import logging
from urllib.parse import unquote

from fastapi import APIRouter, HTTPException, status
from fastapi.responses import Response
from minio.error import S3Error

from search_service.infrastructure.minio_client import minio_client

logger = logging.getLogger(__name__)
image_router = APIRouter()


@image_router.get(
    "/{object_name:path}",
    status_code=status.HTTP_200_OK,
    summary="Get image by object name",
    response_class=Response,
    responses={
        200: {
            "content": {
                "image/jpeg": {},
                "image/png": {},
                "image/gif": {},
                "image/webp": {},
            },
            "description": "Image file",
        },
        404: {"description": "Image not found"},
    },
)
async def get_image(object_name: str) -> Response:
    decoded_object_name = unquote(object_name)
    
    logger.info(
        "Image retrieval request",
        extra={
            "original": object_name,
            "decoded": decoded_object_name,
        }
    )
    
    try:
        image_data, content_type = minio_client.get_image(decoded_object_name)
        return Response(
            content=image_data,
            media_type=content_type,
            headers={
                "Content-Disposition": f'inline; filename="{decoded_object_name.split("/")[-1]}"',
            },
        )
    except S3Error as e:
        logger.error(
            "S3Error retrieving image",
            extra={
                "error_code": e.code,
                "error_message": str(e),
                "object_name": decoded_object_name,
            }
        )
        if e.code == "NoSuchKey":
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=(
                    f"Image not found: {decoded_object_name}. "
                    "This may be due to data inconsistency. "
                    "Please re-upload the image or contact support."
                ),
            )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving image: {str(e)}",
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unexpected error: {str(e)}",
        )

