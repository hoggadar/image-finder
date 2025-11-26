import logging
from typing import List

import httpx

from vector_loader_service.config import config

logger = logging.getLogger(__name__)


class ClipClient:
    def __init__(self):
        self.base_url = config.clip_service.base_url

    async def get_image_embedding(self, image_data: bytes, filename: str) -> List[float]:
        try:
            logger.info(f"Sending request to CLIP service: {self.base_url}/api/v1/clip/embeddings")
            files = {
                "image": (filename, image_data, "image/jpeg")
            }
            data = {
                "text": "placeholder"
            }
            
            async with httpx.AsyncClient(timeout=60.0) as client:
                response = await client.post(
                    f"{self.base_url}/api/v1/clip/embeddings",
                    files=files,
                    data=data,
                )
                
                if response.status_code != 200:
                    logger.error(f"CLIP service returned error: {response.status_code}, body: {response.text}")
                    raise RuntimeError(f"CLIP service error: {response.status_code}")
                
                result = response.json()
                embedding = result["image_embedding"]
                logger.info(f"Successfully received embedding from CLIP service, dimension: {len(embedding)}")
                return embedding
                
        except httpx.RequestError as e:
            logger.error(f"Failed to reach CLIP service at {self.base_url}: {e}")
            raise
        except Exception as e:
            logger.error(f"Error getting image embedding: {e}", exc_info=True)
            raise


clip_client = ClipClient()

