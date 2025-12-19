"""Interface for vector search service."""

from abc import ABC, abstractmethod
from typing import List

from search_service.core.dto.search_result_dto import SearchResultItemDTO


class VectorSearchService(ABC):
    """Interface for vector similarity search."""

    @abstractmethod
    async def search_by_vector(
        self,
        vector: List[float],
        limit: int = 20,
        user_id: str | None = None,
        query_text: str | None = None,  # For logging purposes
    ) -> List[SearchResultItemDTO]:
        """
        Search for similar vectors in the database.
        
        Args:
            vector: Query vector
            limit: Maximum number of results to return
            user_id: Optional user ID to filter results
            
        Returns:
            List of search result items sorted by similarity
        """
        pass

