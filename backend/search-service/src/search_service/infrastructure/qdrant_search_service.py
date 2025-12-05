"""Qdrant vector search implementation."""

import logging
from typing import List, Optional

from qdrant_client import QdrantClient as QdrantClientSDK
from qdrant_client.models import Filter, FieldCondition, MatchValue

from search_service.config import config
from search_service.core.dto.search_result_dto import SearchResultItemDTO
from search_service.core.interface.service.vector_search_service import VectorSearchService

logger = logging.getLogger(__name__)


class QdrantSearchService(VectorSearchService):
    """Qdrant implementation of vector search service."""

    def __init__(self):
        logger.info(
            "Initializing Qdrant search service",
            extra={
                "host": config.qdrant.host,
                "port": config.qdrant.port,
                "collection": config.qdrant.collection_name,
            }
        )
        self.client: QdrantClientSDK = QdrantClientSDK(
            host=config.qdrant.host,
            port=config.qdrant.port,
        )
        self.collection_name = config.qdrant.collection_name

    async def search_by_vector(
        self,
        vector: List[float],
        limit: int = 20,
        user_id: Optional[str] = None,
    ) -> List[SearchResultItemDTO]:
        """
        Search for similar vectors in Qdrant.
        
        Args:
            vector: Query vector
            limit: Maximum number of results to return
            user_id: Optional user ID to filter results
            
        Returns:
            List of search result items sorted by similarity
        """
        try:
            logger.info(
                "Searching vectors in Qdrant",
                extra={
                    "limit": limit,
                    "user_id": user_id,
                    "vector_dimension": len(vector),
                }
            )

            # Prepare filter if user_id is provided
            query_filter = None
            if user_id:
                query_filter = Filter(
                    must=[
                        FieldCondition(
                            key="user_id",
                            match=MatchValue(value=user_id)
                        )
                    ]
                )

            # Perform search
            search_result = self.client.search(
                collection_name=self.collection_name,
                query_vector=vector,
                query_filter=query_filter,
                limit=limit,
            )

            # Convert results to DTOs
            results = [
                SearchResultItemDTO(
                    object_name=hit.payload.get("object_name", ""),
                    image_filename=hit.payload.get("image_filename", ""),
                    user_id=hit.payload.get("user_id", ""),
                    score=hit.score,
                    point_id=str(hit.id),
                )
                for hit in search_result
            ]

            logger.info(
                "Search completed",
                extra={
                    "results_count": len(results),
                    "user_id": user_id,
                }
            )

            return results

        except Exception as e:
            logger.error(
                "Error searching vectors in Qdrant",
                extra={"error": str(e), "user_id": user_id},
                exc_info=True,
            )
            raise


# Global instance
qdrant_search_service = QdrantSearchService()

