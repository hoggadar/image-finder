from dataclasses import dataclass
from typing import List


@dataclass
class SearchResultItemDTO:
    object_name: str
    image_filename: str
    user_id: str
    score: float
    point_id: str


@dataclass
class SearchResultDTO:
    query: str
    items: List[SearchResultItemDTO]
    total_results: int

