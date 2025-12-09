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
    """Background loader for CLIP model to avoid blocking API startup."""
    
    def __init__(self):
        self._model: CLIPModel | None = None
        self._processor: CLIPProcessor | None = None
        self._service: ClipService | None = None
        self._loading = False
        self._loaded = False
        self._error: Exception | None = None
        self._lock = threading.Lock()
    
    def start_loading(self):
        """Start loading the model in a background thread."""
        with self._lock:
            if self._loading or self._loaded:
                return
            self._loading = True
        
        thread = threading.Thread(target=self._load_model, daemon=True)
        thread.start()
    
    def _load_model(self):
        """Load the model (runs in background thread)."""
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
        """Get the CLIP service, raising 503 if not ready."""
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


# Global loader instance
_loader = ClipModelLoader()


def start_model_loading():
    """Start loading the model in background. Call this at app startup."""
    _loader.start_loading()


def is_model_ready() -> bool:
    """Check if the model is ready."""
    return _loader.is_ready


def get_clip_service() -> ClipService:
    """Dependency that returns the CLIP service or 503 if not ready."""
    return _loader.get_service()


ClipServiceDepends = Annotated[ClipService, Depends(get_clip_service)]

__all__ = [
    "ClipServiceDepends",
    "get_clip_service",
    "start_model_loading",
    "is_model_ready",
]

