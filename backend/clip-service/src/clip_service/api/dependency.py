from typing import Annotated
import logging
import threading

from fastapi import Depends, HTTPException, status
from transformers import CLIPModel, CLIPProcessor

from clip_service.app.service import ClipServiceImpl
from clip_service.config import config
from clip_service.core.interface.service import ClipService

logger = logging.getLogger(__name__)


class ClipModelLoader:
    def __init__(self):
        self._model: CLIPModel | None = None
        self._processor: CLIPProcessor | None = None
        self._service: ClipService | None = None
        self._loading = False
        self._loaded = False
        self._error: Exception | None = None
        self._lock = threading.Lock()
    
    def start_loading(self):
        with self._lock:
            if self._loading or self._loaded:
                return
            self._loading = True
        
        thread = threading.Thread(target=self._load_model, daemon=True)
        thread.start()
    
    def _load_model(self):
        try:
            logger.info(f"Starting to load CLIP model: {config.clip_model.model_name}")
            self._model = CLIPModel.from_pretrained(config.clip_model.model_name)
            logger.info("CLIP model loaded from pretrained")
            self._model.eval()
            logger.info("CLIP model set to eval mode")
            
            logger.info(f"Starting to load CLIP processor: {config.clip_model.model_name}")
            self._processor = CLIPProcessor.from_pretrained(config.clip_model.model_name)
            logger.info("CLIP processor loaded from pretrained")
            
            self._service = ClipServiceImpl(model=self._model, processor=self._processor)
            
            with self._lock:
                self._loaded = True
                self._loading = False
            
            logger.info("CLIP model ready to serve requests")
        except Exception as e:
            logger.error(f"Failed to load CLIP model: {e}", exc_info=True)
            with self._lock:
                self._error = e
                self._loading = False
    
    @property
    def is_ready(self) -> bool:
        return self._loaded
    
    @property
    def is_loading(self) -> bool:
        return self._loading
    
    def get_service(self) -> ClipService:
        if self._error:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=f"Model failed to load: {self._error}"
            )
        if not self._loaded:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Model is still loading, please try again shortly"
            )
        return self._service


_loader = ClipModelLoader()


def start_model_loading():
    _loader.start_loading()


def is_model_ready() -> bool:
    return _loader.is_ready


def get_clip_service() -> ClipService:
    return _loader.get_service()


ClipServiceDepends = Annotated[ClipService, Depends(get_clip_service)]

__all__ = [
    "ClipServiceDepends",
    "get_clip_service",
    "start_model_loading",
    "is_model_ready",
]

