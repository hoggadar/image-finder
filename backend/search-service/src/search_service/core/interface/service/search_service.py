"""Interface for main search service."""

from abc import ABC, abstractmethod

from search_service.core.dto.search_result_dto import SearchResultDTO


class SearchService(ABC):
    """Interface for image search service."""

    @abstractmethod
    async def search_images(
        self,
        query: str,
        limit: int = 20,
        user_id: str | None = None,
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
        pass

