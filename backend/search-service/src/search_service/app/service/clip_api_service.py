from __future__ import annotations

import logging
from typing import Dict, List

from search_service.app.service.base_api_service import BaseApiService
from search_service.core.interface.service.clip_api_service import ClipApiService

logger = logging.getLogger(__name__)


class ClipApiServiceImpl(BaseApiService, ClipApiService):
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

    async def get_text_embedding(self, text: str) -> List[float]:
        logger.info(
            "Requesting text embedding from CLIP service",
            extra={"text_length": len(text)}
        )

        data = {"text": text}

        try:
            response = await self.post(
                self._endpoints["GetTextEmbedding"],
                data=data,
            )
        except Exception as e:
            logger.error(
                "Failed to get text embedding from CLIP service",
                extra={
                    "text_length": len(text),
                    "error": str(e),
                    "endpoint": self._endpoints["GetTextEmbedding"],
                }
            )
            raise

        embedding = response["text_embedding"]
        
        logger.info(
            "Successfully received text embedding from CLIP service",
            extra={
                "text_length": len(text),
                "embedding_dimension": len(embedding),
            }
        )

        return embedding

