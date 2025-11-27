import logging

from fastapi import APIRouter, File, Form, HTTPException, UploadFile, status

from upload_service.api.tags import ApiTags
from upload_service.infrastructure.message_broker.rabbitmq_client import rabbitmq_client


logger = logging.getLogger(__name__)

upload_router = APIRouter(tags=[ApiTags.UPLOAD])


@upload_router.post(
    "",
    status_code=status.HTTP_200_OK,
    summary="Upload image to gallery",
    description="Upload an image file. The image will be sent to message queue for storage and processing.",
)
async def upload_image(
    file: UploadFile = File(..., description="Image file to upload"),
    user_id: str = Form(..., description="ID of the user uploading the image"),
):
    """
    Upload an image to user's gallery.
    
    The uploaded image will be:
    1. Validated (must be an image file)
    2. Sent to RabbitMQ message queue
    3. Processed by image-loader-service (saves to MinIO)
    4. Processed by vector-loader-service (generates CLIP embeddings)
    """
    if not file.content_type or not file.content_type.startswith("image/"):
        logger.warning(
            "Invalid file type uploaded",
            extra={
                "user_id": user_id,
                "image_filename": file.filename,
                "content_type": file.content_type,
            }
        )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File must be an image"
        )

    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="user_id is required"
        )

    try:
        image_data = await file.read()
        
        if len(image_data) == 0:
            logger.warning(
                "Empty file uploaded",
                extra={
                    "user_id": user_id,
                    "image_filename": file.filename,
                }
            )
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="File is empty"
            )

        logger.info(
            "Uploading image to message queue",
            extra={
                "user_id": user_id,
                "image_filename": file.filename,
                "size": len(image_data),
                "content_type": file.content_type,
            }
        )

        await rabbitmq_client.publish_image(
            image_data=image_data,
            filename=file.filename or "unknown",
            user_id=user_id,
        )

        logger.info(
            "Image uploaded successfully",
            extra={
                "user_id": user_id,
                "image_filename": file.filename,
                "size": len(image_data),
            }
        )

        return {
            "message": "Image uploaded successfully",
            "filename": file.filename,
            "size": len(image_data),
            "user_id": user_id,
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.exception(
            "Error uploading image",
            extra={
                "user_id": user_id,
                "image_filename": file.filename,
                "error": str(e),
            }
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to upload image: {str(e)}"
        )

