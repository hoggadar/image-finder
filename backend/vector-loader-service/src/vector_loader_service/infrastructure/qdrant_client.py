import logging
from typing import List
from uuid import uuid4

from qdrant_client import QdrantClient as QdrantClientSDK
from qdrant_client.models import Distance, VectorParams, PointStruct

from vector_loader_service.config import config

logger = logging.getLogger(__name__)


class QdrantClient:
    def __init__(self):
        logger.info(f"Initializing Qdrant client: {config.qdrant.host}:{config.qdrant.port}")
        self.client: QdrantClientSDK = QdrantClientSDK(
            host=config.qdrant.host,
            port=config.qdrant.port,
        )
        self._ensure_collection_exists()

    def _ensure_collection_exists(self) -> None:
        try:
            collections = self.client.get_collections().collections
            collection_names = [c.name for c in collections]
            
            if config.qdrant.collection_name not in collection_names:
                logger.info(f"Creating collection: {config.qdrant.collection_name}")
                self.client.create_collection(
                    collection_name=config.qdrant.collection_name,
                    vectors_config=VectorParams(
                        size=config.qdrant.vector_size,
                        distance=Distance.COSINE,
                    ),
                )
                logger.info(f"Collection created: {config.qdrant.collection_name}")
            else:
                logger.info(f"Collection already exists: {config.qdrant.collection_name}")
        except Exception as e:
            logger.error(f"Error ensuring collection exists: {e}", exc_info=True)
            raise

    def store_vector(
        self,
        vector: List[float],
        user_id: str,
        object_name: str,
        image_filename: str,
    ) -> str:
        try:
            point_id = str(uuid4())
            logger.info(f"Preparing to store vector: point_id={point_id}, user_id={user_id}, object_name={object_name}")
            
            point = PointStruct(
                id=point_id,
                vector=vector,
            payload={
                "user_id": user_id,
                "object_name": object_name,
                "image_filename": image_filename,
            },
            )
            
            logger.info(f"Upserting point to collection: {config.qdrant.collection_name}")
            self.client.upsert(
                collection_name=config.qdrant.collection_name,
                points=[point],
            )
            logger.info(f"Successfully stored vector in Qdrant: point_id={point_id}")
            
            return point_id
        except Exception as e:
            logger.error(f"Error storing vector in Qdrant: {e}", exc_info=True)
            raise


qdrant_client = QdrantClient()

