import logging

from fastapi import APIRouter, File, UploadFile, status, HTTPException
import httpx

from api_gateway.api.dependency import CurrentUserIdDep
from api_gateway.api.security import require_roles
from api_gateway.config import config

logger = logging.getLogger(__name__)

upload_router = APIRouter()


def _find_upload_service_url() -> str:
    for service in config.services:
        if service.name == "upload-service":
            return service.base_url
    return "http://upload-service:8080"


@upload_router.post(
    "/upload",
    status_code=status.HTTP_200_OK,
)
@require_roles("Admin")
async def upload_image(file: UploadFile = File(...), user_id: str = CurrentUserIdDep) -> dict:
    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File must be an image"
        )

    try:
        image_data = await file.read()
        
        if len(image_data) == 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="File is empty"
            )

        upload_service_url = _find_upload_service_url()
        upload_endpoint = f"{upload_service_url}/v1/upload"
        
        files = {
            "file": (file.filename or "unknown", image_data, file.content_type)
        }
        data = {
            "user_id": user_id
        }
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                upload_endpoint,
                files=files,
                data=data,
            )
            
            if response.status_code >= 400:
                logger.error(
                    f"Upload service returned error: {response.status_code}",
                    extra={"response": response.text}
                )
                raise HTTPException(
                    status_code=response.status_code,
                    detail=response.json() if response.headers.get("content-type", "").startswith("application/json") else response.text
                )
            
            result = response.json()
            logger.info(f"Image '{file.filename}' uploaded successfully for user {user_id}")
            return result
            
    except httpx.RequestError as e:
        logger.error(f"Failed to reach upload service: {e}")
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Upload service unavailable"
        )
    except Exception as e:
        logger.error(f"Error uploading image: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to upload image: {str(e)}"
        )

