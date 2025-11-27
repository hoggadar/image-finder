import logging

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status

from api_gateway.api.dependency import UploadApiServiceDep, get_current_user_id_from_token
from api_gateway.api.security import require_roles
from api_gateway.api.tags import ApiTags
from api_gateway.api.v1.schema.auth import TokenValidationResponse

logger = logging.getLogger(__name__)

upload_router = APIRouter(tags=[ApiTags.UPLOAD])


@upload_router.post(
    "",
    status_code=status.HTTP_200_OK,
    summary="Upload image to gallery",
    description="Upload an image file. Requires authentication with User, Admin, or Moderator role.",
)
async def upload_image(
    upload_service: UploadApiServiceDep,
    file: UploadFile = File(..., description="Image file to upload"),
    token_data: TokenValidationResponse = Depends(require_roles("User", "Admin", "Moderator")),
) -> dict:
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

    await file.seek(0)
    
    user_id = get_current_user_id_from_token(token_data)
    
    result = await upload_service.upload_image(file, user_id)
    logger.info(f"Image '{file.filename}' uploaded successfully for user {user_id}")
    return result

