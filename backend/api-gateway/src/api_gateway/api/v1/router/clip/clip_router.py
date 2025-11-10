from fastapi import APIRouter, File, Form, UploadFile, status

from api_gateway.api.v1.schema.clip import (
    ClipSimilarityResponse,
    CompareEmbeddingsRequest,
    CompareEmbeddingsResponse,
    CompareTextWithImageVectorRequest,
    EmbeddingsResponse,
)


clip_router = APIRouter()


@clip_router.post(
    "/similarity",
    status_code=status.HTTP_200_OK,
    summary="Calculate similarity between an image and a text prompt",
    response_model=ClipSimilarityResponse,
)
async def calculate_similarity(
    image: UploadFile = File(..., description="Image for analysis"),
    text: str = Form(..., description="Text description for comparison"),
) -> ClipSimilarityResponse:
    raise NotImplementedError("Gateway proxy for similarity calculation is not implemented yet")


@clip_router.post(
    "/embeddings",
    status_code=status.HTTP_200_OK,
    summary="Return embeddings for both image and text inputs",
    response_model=EmbeddingsResponse,
)
async def get_embeddings(
    image: UploadFile = File(..., description="Image for embedding generation"),
    text: str = Form(..., description="Text prompt for embedding generation"),
) -> EmbeddingsResponse:
    raise NotImplementedError("Gateway proxy for embedding generation is not implemented yet")


@clip_router.post(
    "/similarity/embeddings",
    status_code=status.HTTP_200_OK,
    summary="Compare similarity between provided image and text embeddings",
    response_model=CompareEmbeddingsResponse,
)
async def compare_embeddings(payload: CompareEmbeddingsRequest) -> CompareEmbeddingsResponse:
    raise NotImplementedError("Gateway proxy for embedding comparison is not implemented yet")


@clip_router.post(
    "/similarity/text-image-vector",
    status_code=status.HTTP_200_OK,
    summary="Compare a text prompt against a provided image embedding",
    response_model=CompareEmbeddingsResponse,
)
async def compare_text_with_image_vector(
    payload: CompareTextWithImageVectorRequest,
) -> CompareEmbeddingsResponse:
    raise NotImplementedError("Gateway proxy for text-image comparison is not implemented yet")

