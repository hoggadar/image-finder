import torch
from fastapi import APIRouter, File, Form, UploadFile, status

from clip_service.api.dependency import ClipServiceDepends
from clip_service.api.v1.schema import (
    ClipSimilarityResponse,
    CompareEmbeddingsRequest,
    CompareEmbeddingsResponse,
    CompareTextWithImageVectorRequest,
    EmbeddingsResponse,
    ImageEmbeddingResponse,
)


clip_router = APIRouter()


@clip_router.post(
    "/similarity",
    status_code=status.HTTP_200_OK,
    summary="Calculate similarity between an image and a text prompt",
    response_model=ClipSimilarityResponse,
)
async def calculate_similarity(
    clip_service: ClipServiceDepends,
    image: UploadFile = File(..., description="Image for analysis"),
    text: str = Form(..., description="Text description for comparison"),
) -> ClipSimilarityResponse:
    image_bytes = await image.read()
    result = await clip_service.calculate_similarity(image_bytes=image_bytes, text=text)
    return ClipSimilarityResponse(**result.model_dump())


@clip_router.post(
    "/embeddings",
    status_code=status.HTTP_200_OK,
    summary="Return embeddings for both image and text inputs",
    response_model=EmbeddingsResponse,
)
async def get_embeddings(
    clip_service: ClipServiceDepends,
    image: UploadFile = File(..., description="Image for embedding generation"),
    text: str = Form(..., description="Text prompt for embedding generation"),
) -> EmbeddingsResponse:
    image_bytes = await image.read()
    image_embedding, text_embedding = await clip_service.get_embeddings(image_bytes=image_bytes, text=text)
    return EmbeddingsResponse(
        image_embedding=image_embedding.detach().cpu().tolist(),
        text_embedding=text_embedding.detach().cpu().tolist(),
    )


@clip_router.post(
    "/similarity/embeddings",
    status_code=status.HTTP_200_OK,
    summary="Compare similarity between provided image and text embeddings",
    response_model=CompareEmbeddingsResponse,
)
async def compare_embeddings(
    clip_service: ClipServiceDepends,
    payload: CompareEmbeddingsRequest,
) -> CompareEmbeddingsResponse:
    image_embedding = torch.tensor(payload.image_embedding, dtype=torch.float32)
    text_embedding = torch.tensor(payload.text_embedding, dtype=torch.float32)
    similarity, distance = await clip_service.compare_embeddings(
        image_embedding=image_embedding,
        text_embedding=text_embedding,
    )
    return CompareEmbeddingsResponse(similarity=similarity, distance=distance)


@clip_router.post(
    "/similarity/text-image-vector",
    status_code=status.HTTP_200_OK,
    summary="Compare a text prompt against a provided image embedding",
    response_model=CompareEmbeddingsResponse,
)
async def compare_text_with_image_vector(
    clip_service: ClipServiceDepends,
    payload: CompareTextWithImageVectorRequest,
) -> CompareEmbeddingsResponse:
    image_embedding = torch.tensor(payload.image_embedding, dtype=torch.float32)
    similarity, distance = await clip_service.compare_text_with_image_vector(
        text=payload.text,
        image_embedding=image_embedding,
    )
    return CompareEmbeddingsResponse(similarity=similarity, distance=distance)


@clip_router.post(
    "/image-embedding",
    status_code=status.HTTP_200_OK,
    summary="Get embedding for an image only",
    response_model=ImageEmbeddingResponse,
)
async def get_image_embedding(
    clip_service: ClipServiceDepends,
    image: UploadFile = File(..., description="Image for embedding generation"),
) -> ImageEmbeddingResponse:
    """Get embedding vector for an image without requiring text input."""
    image_bytes = await image.read()
    image_embedding = await clip_service.get_image_embedding(image_bytes=image_bytes)
    return ImageEmbeddingResponse(
        image_embedding=image_embedding.detach().cpu().tolist()
    )