import logging

from fastapi import APIRouter, File, UploadFile, status, HTTPException

from api_gateway.api.dependency import CurrentUserIdDep, UploadApiServiceDep
from api_gateway.api.security import require_roles
from api_gateway.api.tags import ApiTags

logger = logging.getLogger(__name__)

upload_router = APIRouter(tags=[ApiTags.UPLOAD])


@upload_router.post(
    "/upload",
    status_code=status.HTTP_200_OK,
)
async def upload_image(
    upload_service: UploadApiServiceDep,
    file: UploadFile = File(...),
    user_id: str = CurrentUserIdDep,
) -> dict:
    """Upload an image file to the storage service."""
    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File must be an image"
        )

    image_data = await file.read()
    
    if len(image_data) == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File is empty"
        )

    # Reset file position after reading for the service to re-read
    await file.seek(0)
    
    result = await upload_service.upload_image(file, user_id)
    logger.info(f"Image '{file.filename}' uploaded successfully for user {user_id}")
    return result

