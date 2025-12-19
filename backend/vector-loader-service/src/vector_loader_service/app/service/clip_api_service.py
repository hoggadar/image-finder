from __future__ import annotations

import logging
from typing import Any, Dict, List

from vector_loader_service.app.service.base_api_service import BaseApiServiceImpl
from vector_loader_service.core.interface.service.clip_api_service import ClipApiService


logger = logging.getLogger(__name__)


class ClipApiServiceImpl(BaseApiServiceImpl, ClipApiService):
    def __init__(
        self, 
        base_url: str, 
        endpoints: Dict[str, str], 
        *, 
        timeout: float = 30.0,
        max_retries: int = 3,
        retry_delay: float = 2.0,
    ) -> None:
        super().__init__(
            base_url=base_url, 
            timeout=timeout, 
            max_retries=max_retries, 
            retry_delay=retry_delay
        )
        self._endpoints = endpoints

    async def get_image_embedding(
        self, image_data: bytes, image_filename: str
    ) -> List[float]:
        logger.info(
            "Requesting image embedding from CLIP service",
            extra={
                "image_filename": image_filename,
                "size": len(image_data),
                "endpoint": self._endpoints["GetImageEmbedding"],
            }
        )

        files = {"image": (image_filename, image_data, "image/jpeg")}

        try:
            response = await self.post(
                self._endpoints["GetImageEmbedding"],
                files=files,
            )
        except Exception as e:
            logger.error(
                "Failed to get image embedding from CLIP service",
                extra={
                    "image_filename": image_filename,
                    "error": str(e),
                    "endpoint": self._endpoints["GetImageEmbedding"],
                }
            )
            raise

        embedding = response["image_embedding"]
        
        logger.info(
            "Successfully received image embedding from CLIP service",
            extra={
                "image_filename": image_filename,
                "embedding_dimension": len(embedding),
            }
        )

        return embedding

    async def get_text_embedding(self, text: str) -> List[float]:
        logger.debug(
            "Requesting text embedding from CLIP service",
            extra={"text_length": len(text)}
        )

        import io
        from PIL import Image
        
        img = Image.new('RGB', (1, 1), color='white')
        img_bytes = io.BytesIO()
        img.save(img_bytes, format='JPEG')
        img_bytes.seek(0)

        files = {"image": ("placeholder.jpg", img_bytes.read(), "image/jpeg")}
        data = {"text": text}

        response = await self.post(
            self._endpoints["GetEmbeddings"],
            data=data,
            files=files,
        )

        embedding = response["text_embedding"]
        
        logger.info(
            "Successfully received text embedding from CLIP service",
            extra={
                "text_length": len(text),
                "embedding_dimension": len(embedding),
            }
        )

        return embedding

