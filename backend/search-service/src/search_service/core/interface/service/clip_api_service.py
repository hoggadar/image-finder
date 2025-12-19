from abc import ABC, abstractmethod
from typing import List


class ClipApiService(ABC):
    @abstractmethod
    async def get_text_embedding(self, text: str) -> List[float]:
        pass

