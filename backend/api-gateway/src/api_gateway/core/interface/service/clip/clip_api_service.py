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
    """Abstraction describing gateway operations for the CLIP microservice."""

    @abstractmethod
    async def calculate_similarity(
        self, image: UploadFile, text: str
    ) -> ClipSimilarityResponse:
        """Calculate similarity between an image and a text prompt."""

    @abstractmethod
    async def get_embeddings(self, image: UploadFile, text: str) -> EmbeddingsResponse:
        """Return embeddings for both image and text inputs."""

    @abstractmethod
    async def compare_embeddings(
        self, payload: CompareEmbeddingsRequest
    ) -> CompareEmbeddingsResponse:
        """Compare similarity between provided image and text embeddings."""

    @abstractmethod
    async def compare_text_with_image_vector(
        self, payload: CompareTextWithImageVectorRequest
    ) -> CompareEmbeddingsResponse:
        """Compare a text prompt against a provided image embedding."""

