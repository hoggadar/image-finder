from typing import List

from pydantic import BaseModel, Field


class EmbeddingsResponse(BaseModel):
    image_embedding: List[float] = Field(..., description="Vector representation of the uploaded image")
    text_embedding: List[float] = Field(..., description="Vector representation of the provided text")


class CompareEmbeddingsRequest(BaseModel):
    image_embedding: List[float] = Field(..., description="Embedding representing an image")
    text_embedding: List[float] = Field(..., description="Embedding representing a text prompt")


class CompareTextWithImageVectorRequest(BaseModel):
    text: str = Field(..., description="Text prompt to embed and compare")
    image_embedding: List[float] = Field(..., description="Embedding representing an image")


class CompareEmbeddingsResponse(BaseModel):
    similarity: float = Field(..., description="Cosine similarity between the provided embeddings")
    distance: float = Field(..., description="Distance score where lower values denote better matches")


class ClipSimilarityResponse(BaseModel):
    similarity: float = Field(..., description="Cosine similarity between image and text embeddings")
    distance: float = Field(..., description="Distance score where 0 denotes perfect match")
    probability: float = Field(..., description="Derived probability score based on distance")
    interpretation: str = Field(..., description="Human-friendly interpretation of similarity score")
    text: str = Field(..., description="Original text prompt that was evaluated")
    image_width: int = Field(..., description="Width of the processed image in pixels")
    image_height: int = Field(..., description="Height of the processed image in pixels")
    embedding_dim: int = Field(..., description="Dimensionality of the generated embeddings")


