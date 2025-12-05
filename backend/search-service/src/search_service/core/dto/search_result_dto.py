"""Data transfer objects for search results."""

from dataclasses import dataclass
from typing import List


@dataclass
class SearchResultItemDTO:
    """Single search result item."""
    object_name: str
    image_filename: str
    user_id: str
    score: float  # Similarity score
    point_id: str


@dataclass
class SearchResultDTO:
    """Search results with metadata."""
    query: str
    items: List[SearchResultItemDTO]
    total_results: int

