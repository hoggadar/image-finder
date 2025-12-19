from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from fastapi import UploadFile

from api_gateway.api.v1.schema.clip import (
    ClipSimilarityResponse,
    CompareEmbeddingsRequest,
    CompareEmbeddingsResponse,
    CompareTextWithImageVectorRequest,
    EmbeddingsResponse,
)
from api_gateway.core.interface.service.base_api_service import BaseApiService


class ClipApiService(BaseApiService, ABC):
    @abstractmethod
    async def calculate_similarity(
        self, image: UploadFile, text: str
    ) -> ClipSimilarityResponse:
        pass

    @abstractmethod
    async def get_embeddings(self, image: UploadFile, text: str) -> EmbeddingsResponse:
        pass

    @abstractmethod
    async def compare_embeddings(
        self, payload: CompareEmbeddingsRequest
    ) -> CompareEmbeddingsResponse:
        pass

    @abstractmethod
    async def compare_text_with_image_vector(
        self, payload: CompareTextWithImageVectorRequest
    ) -> CompareEmbeddingsResponse:
        pass

