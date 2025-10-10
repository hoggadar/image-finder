from abc import ABC, abstractmethod
from typing import Sequence, Optional

class BaseRepository[Entity, ID](ABC):
    @abstractmethod
    async def get_all(self, offset: int = 0, limit: int = 10, search: str = "") -> Sequence[Entity]:
        pass
    
    @abstractmethod
    async def get_by_id(self, id: ID) -> Optional[Entity]:
        pass
    
    @abstractmethod
    async def create(self, entity: Entity) -> Optional[Entity]:
        pass
    
    @abstractmethod
    async def update(self, entity: Entity) -> Optional[Entity]:
        pass
    
    @abstractmethod
    async def delete(self, id: ID) -> Optional[Entity]:
        pass