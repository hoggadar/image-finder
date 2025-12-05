"""Main search service implementation."""

import logging
from typing import Optional

from search_service.core.dto.search_result_dto import SearchResultDTO
from search_service.core.exception import EmptyQueryException
from search_service.core.interface.service.clip_api_service import ClipApiService
from search_service.core.interface.service.search_service import SearchService as ISearchService
from search_service.core.interface.service.vector_search_service import VectorSearchService

logger = logging.getLogger(__name__)


class SearchServiceImpl(ISearchService):
    """Implementation of image search service."""

    def __init__(
        self,
        clip_service: ClipApiService,
        vector_search_service: VectorSearchService,
    ):
        self.clip_service = clip_service
        self.vector_search_service = vector_search_service

    async def search_images(
        self,
        query: str,
        limit: int = 20,
        user_id: Optional[str] = None,
    ) -> SearchResultDTO:
        """
        Search for images by text query.
        
        Args:
            query: Text description to search for
            limit: Maximum number of results to return
            user_id: Optional user ID to filter results to specific user
            
        Returns:
            Search results with metadata
        """
        if not query or not query.strip():
            raise EmptyQueryException()

        logger.info(
            "Starting image search",
            extra={
                "query": query[:100],
                "limit": limit,
                "user_id": user_id,
            }
        )

        # Get text embedding from CLIP
        text_embedding = await self.clip_service.get_text_embedding(query)

        # Search similar vectors in Qdrant
        results = await self.vector_search_service.search_by_vector(
            vector=text_embedding,
            limit=limit,
            user_id=user_id,
        )

        logger.info(
            "Search completed",
            extra={
                "query": query[:100],
                "results_count": len(results),
            }
        )

        return SearchResultDTO(
            query=query,
            items=results,
            total_results=len(results),
        )

