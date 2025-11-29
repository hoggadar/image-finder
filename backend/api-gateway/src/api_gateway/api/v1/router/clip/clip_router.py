from fastapi import APIRouter, File, Form, UploadFile, status

from api_gateway.api.dependency import ClipApiServiceDep
from api_gateway.api.tags import ApiTags
from api_gateway.api.v1.schema.clip import (
    ClipSimilarityResponse,
    CompareEmbeddingsRequest,
    CompareEmbeddingsResponse,
    CompareTextWithImageVectorRequest,
    EmbeddingsResponse,
)


clip_router = APIRouter(tags=[ApiTags.CLIP])


@clip_router.post(
    "/similarity",
    status_code=status.HTTP_200_OK,
    summary="Calculate similarity between an image and a text prompt",
    response_model=ClipSimilarityResponse,
)
async def calculate_similarity(
    clip_service: ClipApiServiceDep,
    image: UploadFile = File(..., description="Image for analysis"),
    text: str = Form(..., description="Text description for comparison"),
) -> ClipSimilarityResponse:
    return await clip_service.calculate_similarity(image, text)


@clip_router.post(
    "/embeddings",
    status_code=status.HTTP_200_OK,
    summary="Return embeddings for both image and text inputs",
    response_model=EmbeddingsResponse,
)
async def get_embeddings(
    clip_service: ClipApiServiceDep,
    image: UploadFile = File(..., description="Image for embedding generation"),
    text: str = Form(..., description="Text prompt for embedding generation"),
) -> EmbeddingsResponse:
    return await clip_service.get_embeddings(image, text)


@clip_router.post(
    "/similarity/embeddings",
    status_code=status.HTTP_200_OK,
    summary="Compare similarity between provided image and text embeddings",
    response_model=CompareEmbeddingsResponse,
)
async def compare_embeddings(
    clip_service: ClipApiServiceDep,
    payload: CompareEmbeddingsRequest,
) -> CompareEmbeddingsResponse:
    return await clip_service.compare_embeddings(payload)


@clip_router.post(
    "/similarity/text-image-vector",
    status_code=status.HTTP_200_OK,
    summary="Compare a text prompt against a provided image embedding",
    response_model=CompareEmbeddingsResponse,
)
async def compare_text_with_image_vector(
    clip_service: ClipApiServiceDep,
    payload: CompareTextWithImageVectorRequest,
) -> CompareEmbeddingsResponse:
    return await clip_service.compare_text_with_image_vector(payload)

