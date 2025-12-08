from functools import lru_cache
from typing import Annotated
import logging

from fastapi import Depends
from transformers import CLIPModel, CLIPProcessor

from clip_service.app.service import ClipServiceImpl
from clip_service.config import config
from clip_service.core.interface.service import ClipService

logger = logging.getLogger(__name__)


@lru_cache
def get_clip_model() -> CLIPModel:
    logger.info(f"Starting to load CLIP model: {config.clip_model.model_name}")
    model = CLIPModel.from_pretrained(config.clip_model.model_name)
    logger.info("CLIP model loaded from pretrained")
    model.eval()
    logger.info("CLIP model set to eval mode")
    return model


@lru_cache
def get_clip_processor() -> CLIPProcessor:
    logger.info(f"Starting to load CLIP processor: {config.clip_model.model_name}")
    processor = CLIPProcessor.from_pretrained(config.clip_model.model_name)
    logger.info("CLIP processor loaded from pretrained")
    return processor


@lru_cache
def get_clip_service() -> ClipService:
    return ClipServiceImpl(model=get_clip_model(), processor=get_clip_processor())


ClipServiceDepends = Annotated[ClipService, Depends(get_clip_service)]

__all__ = [
    "ClipServiceDepends",
    "get_clip_service",
]

