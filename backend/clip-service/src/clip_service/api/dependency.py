from functools import lru_cache
from typing import Annotated

from fastapi import Depends
from transformers import CLIPModel, CLIPProcessor

from clip_service.app.service import ClipServiceImpl
from clip_service.config import config
from clip_service.core.interface.service import ClipService


@lru_cache
def get_clip_model() -> CLIPModel:
    model = CLIPModel.from_pretrained(config.clip_model.model_name)
    model.eval()
    return model


@lru_cache
def get_clip_processor() -> CLIPProcessor:
    return CLIPProcessor.from_pretrained(config.clip_model.model_name)


@lru_cache
def get_clip_service() -> ClipService:
    return ClipServiceImpl(model=get_clip_model(), processor=get_clip_processor())


ClipServiceDepends = Annotated[ClipService, Depends(get_clip_service)]

__all__ = [
    "ClipServiceDepends",
    "get_clip_service",
]

