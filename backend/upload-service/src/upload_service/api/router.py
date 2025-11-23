import logging

from fastapi import APIRouter, File, UploadFile, HTTPException, Form

from upload_service.infrastructure.rabbitmq import rabbitmq_client

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/upload")
async def upload_image(
    file: UploadFile = File(...),
    user_id: str = Form(...),
):
    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(
            status_code=400,
            detail="File must be an image"
        )

    if not user_id:
        raise HTTPException(
            status_code=400,
            detail="user_id is required"
        )

    try:
        image_data = await file.read()
        
        if len(image_data) == 0:
            raise HTTPException(
                status_code=400,
                detail="File is empty"
            )

        await rabbitmq_client.publish_image(
            image_data=image_data,
            filename=file.filename or "unknown",
            user_id=user_id,
        )

        return {
            "message": "Image uploaded successfully",
            "filename": file.filename,
            "size": len(image_data),
            "user_id": user_id,
        }
    except Exception as e:
        logger.error(f"Error uploading image: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to upload image: {str(e)}"
        )

