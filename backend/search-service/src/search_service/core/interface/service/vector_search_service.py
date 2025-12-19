from abc import ABC, abstractmethod
from typing import List

from search_service.core.dto.search_result_dto import SearchResultItemDTO


class VectorSearchService(ABC):
    @abstractmethod
    async def search_by_vector(
        self,
        vector: List[float],
        limit: int = 20,
        user_id: str | None = None,
        query_text: str | None = None,
    ) -> List[SearchResultItemDTO]:
        pass

