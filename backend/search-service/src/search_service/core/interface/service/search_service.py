from abc import ABC, abstractmethod

from search_service.core.dto.search_result_dto import SearchResultDTO


class SearchService(ABC):
    @abstractmethod
    async def search_images(
        self,
        query: str,
        limit: int = 20,
        user_id: str | None = None,
    ) -> SearchResultDTO:
        pass

