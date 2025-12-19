from __future__ import annotations

from typing import Dict

from fastapi import UploadFile

from api_gateway.api.v1.schema.clip import (
    ClipSimilarityResponse,
    CompareEmbeddingsRequest,
    CompareEmbeddingsResponse,
    CompareTextWithImageVectorRequest,
    EmbeddingsResponse,
)
from api_gateway.app.service.base_api_service import BaseApiServiceImpl
from api_gateway.core.interface.service.clip import ClipApiService


class ClipApiServiceImpl(BaseApiServiceImpl, ClipApiService):
    def __init__(
        self, base_url: str, endpoints: Dict[str, str], *, timeout: float = 30.0
    ) -> None:
        super().__init__(base_url=base_url, timeout=timeout)
        self._endpoints = endpoints

    async def calculate_similarity(
        self, image: UploadFile, text: str
    ) -> ClipSimilarityResponse:
        image_data = await image.read()
        files = {"image": (image.filename or "image", image_data, image.content_type)}
        data = {"text": text}

        response = await self.post(
            self._endpoints["GenerateSimilarityReport"],
            data=data,
            files=files,
        )
        return ClipSimilarityResponse(**response)

    async def get_embeddings(
        self, image: UploadFile, text: str
    ) -> EmbeddingsResponse:
        image_data = await image.read()
        files = {"image": (image.filename or "image", image_data, image.content_type)}
        data = {"text": text}

        response = await self.post(
            self._endpoints["GetEmbeddings"],
            data=data,
            files=files,
        )
        return EmbeddingsResponse(**response)

    async def compare_embeddings(
        self, payload: CompareEmbeddingsRequest
    ) -> CompareEmbeddingsResponse:
        response = await self.post(
            self._endpoints["ComparePrecomputedEmbeddings"],
            json=payload.model_dump(),
        )
        return CompareEmbeddingsResponse(**response)

    async def compare_text_with_image_vector(
        self, payload: CompareTextWithImageVectorRequest
    ) -> CompareEmbeddingsResponse:
        response = await self.post(
            self._endpoints["CompareTextWithImageVector"],
            json=payload.model_dump(),
        )
        return CompareEmbeddingsResponse(**response)

