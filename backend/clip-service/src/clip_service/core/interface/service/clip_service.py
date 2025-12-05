from abc import ABC, abstractmethod
from typing import Tuple

from torch import Tensor

from clip_service.core.dto.clip_similarity_dto import ClipSimilarityResultDTO


class ClipService(ABC):
    @abstractmethod
    async def calculate_similarity(self, image_bytes: bytes, text: str) -> ClipSimilarityResultDTO:
        raise NotImplementedError

    @abstractmethod
    async def get_embeddings(self, image_bytes: bytes, text: str) -> Tuple[Tensor, Tensor]:
        raise NotImplementedError

    @abstractmethod
    async def compare_embeddings(self, image_embedding: Tensor, text_embedding: Tensor) -> Tuple[float, float]:
        raise NotImplementedError

    @abstractmethod
    async def compare_text_with_image_vector(self, text: str, image_embedding: Tensor) -> Tuple[float, float]:
        raise NotImplementedError

    @abstractmethod
    async def get_image_embedding(self, image_bytes: bytes) -> Tensor:
        raise NotImplementedError

    @abstractmethod
    async def get_text_embedding(self, text: str) -> Tensor:
        raise NotImplementedError

