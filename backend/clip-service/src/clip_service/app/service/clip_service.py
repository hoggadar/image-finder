import asyncio
import io
import logging
from typing import Final, Tuple

import torch
from PIL import Image, UnidentifiedImageError
from transformers import CLIPModel, CLIPProcessor
from torch import Tensor

from clip_service.app.exception.clip_exception import (
    EmptyTextException,
    InvalidImageException,
    ModelInferenceException,
)
from clip_service.core.dto.clip_similarity_dto import ClipSimilarityResultDTO
from clip_service.core.interface.service import ClipService


class ClipServiceImpl(ClipService):
    PERFECT_MATCH_THRESHOLD: Final[float] = 0.25
    HIGH_MATCH_THRESHOLD: Final[float] = 0.4
    MEDIUM_MATCH_THRESHOLD: Final[float] = 0.6

    def __init__(self, model: CLIPModel, processor: CLIPProcessor) -> None:
        self._model = model
        self._processor = processor
        self._model.eval()
        self._logger = logging.getLogger(__name__)

    async def calculate_similarity(self, image_bytes: bytes, text: str) -> ClipSimilarityResultDTO:
        """Return similarity report for uploaded image and text prompt."""
        self._logger.debug("Starting similarity calculation", extra={"text": text[:50]})
        return await asyncio.to_thread(self._calculate_similarity_sync, image_bytes, text)

    async def get_embeddings(self, image_bytes: bytes, text: str) -> Tuple[Tensor, Tensor]:
        """Produce normalized embeddings for image bytes and accompanying text."""
        return await asyncio.to_thread(self._get_embeddings_sync, image_bytes, text)

    async def compare_embeddings(self, image_embedding: Tensor, text_embedding: Tensor) -> Tuple[float, float]:
        """Calculate similarity metrics for two precomputed embeddings."""
        normalized_image = self._normalize_embedding(image_embedding)
        normalized_text = self._normalize_embedding(text_embedding)
        similarity, distance, _ = self._compute_similarity_metrics(normalized_image, normalized_text)
        return round(similarity, 4), round(distance, 4)

    async def compare_text_with_image_vector(self, text: str, image_embedding: Tensor) -> Tuple[float, float]:
        """Embed text and compare it with a supplied image embedding."""
        normalized_image = self._normalize_embedding(image_embedding)
        text_embedding = await asyncio.to_thread(self._get_text_embedding, text)
        similarity, distance, _ = self._compute_similarity_metrics(normalized_image, text_embedding)
        return round(similarity, 4), round(distance, 4)

    async def get_image_embedding(self, image_bytes: bytes) -> Tensor:
        """Get embedding for an image without requiring text input."""
        return await asyncio.to_thread(self._get_image_embedding_sync, image_bytes)

    def _calculate_similarity_sync(self, image_bytes: bytes, text: str) -> ClipSimilarityResultDTO:
        """Synchronous worker: compute similarity DTO for raw inputs."""
        if not text:
            raise EmptyTextException()

        pil_image = self._load_image(image_bytes)
        image_embedding, text_embedding = self._get_embeddings_from_image(pil_image, text)

        similarity, distance, probability = self._compute_similarity_metrics(image_embedding, text_embedding)
        interpretation = self._interpret_distance(distance)

        result = ClipSimilarityResultDTO(
            similarity=round(similarity, 4),
            distance=round(distance, 4),
            probability=round(probability, 4),
            interpretation=interpretation,
            text=text,
            image_width=pil_image.width,
            image_height=pil_image.height,
            embedding_dim=image_embedding.shape[-1],
        )

        self._logger.debug(
            "Similarity calculation finished",
            extra={
                "similarity": result.similarity,
                "distance": result.distance,
                "probability": result.probability,
                "interpretation": interpretation,
            },
        )

        return result

    def _get_embeddings_sync(self, image_bytes: bytes, text: str) -> Tuple[Tensor, Tensor]:
        """Synchronous worker: build embeddings from raw inputs."""
        if not text:
            raise EmptyTextException()

        pil_image = self._load_image(image_bytes)
        return self._get_embeddings_from_image(pil_image, text)

    def _get_image_embedding_sync(self, image_bytes: bytes) -> Tensor:
        """Synchronous worker: build image embedding from raw image bytes."""
        pil_image = self._load_image(image_bytes)
        return self._get_image_embedding(pil_image)

    def _get_embeddings_from_image(self, pil_image: Image.Image, text: str) -> Tuple[Tensor, Tensor]:
        """Helper: derive image and text embeddings from decoded image."""
        image_embedding = self._get_image_embedding(pil_image)
        text_embedding = self._get_text_embedding(text)
        return image_embedding, text_embedding

    def _load_image(self, image_bytes: bytes) -> Image.Image:
        """Decode image bytes into RGB PIL image, raising on failure."""
        try:
            return Image.open(io.BytesIO(image_bytes)).convert("RGB")
        except UnidentifiedImageError:
            self._logger.exception("Unable to decode provided image")
            raise InvalidImageException()

    def _get_image_embedding(self, image: Image.Image) -> Tensor:
        """Generate normalized embedding for a PIL image."""
        image_inputs = self._processor(images=image, return_tensors="pt")

        try:
            with torch.no_grad():
                image_embeds = self._model.get_image_features(**image_inputs)
        except RuntimeError:
            self._logger.exception("Model inference failed while processing image")
            raise ModelInferenceException()

        return self._normalize_embedding(image_embeds)

    def _get_text_embedding(self, text: str) -> Tensor:
        """Generate normalized embedding for provided text."""
        if not text:
            raise EmptyTextException()

        text_inputs = self._processor(text=[text], return_tensors="pt", padding=True)

        try:
            with torch.no_grad():
                text_embeds = self._model.get_text_features(**text_inputs)
        except RuntimeError:
            self._logger.exception("Model inference failed while processing text")
            raise ModelInferenceException()

        return self._normalize_embedding(text_embeds)

    def _normalize_embedding(self, embedding: Tensor) -> Tensor:
        """Ensure 1-D unit vector representation for similarity math."""
        if embedding.ndim > 1:
            embedding = embedding.squeeze(0)

        norm = embedding.norm(p=2)
        if norm == 0:
            return embedding

        return embedding / norm

    def _compute_similarity_metrics(
        self,
        image_embedding: Tensor,
        text_embedding: Tensor,
    ) -> Tuple[float, float, float]:
        """Return cosine similarity, distance score and derived probability."""
        similarity = float(torch.dot(text_embedding, image_embedding).item())
        distance = max(0.0, (1 - similarity) / 2)
        probability = max(0.0, min(1.0, 1 - distance))
        return similarity, distance, probability

    def _interpret_distance(self, distance: float) -> str:
        if distance <= self.PERFECT_MATCH_THRESHOLD:
            return "Perfect match"
        if distance <= self.HIGH_MATCH_THRESHOLD:
            return "High match"
        if distance <= self.MEDIUM_MATCH_THRESHOLD:
            return "Medium match"
        return "Low match"

