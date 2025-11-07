from pydantic import BaseModel


class ClipSimilarityResultDTO(BaseModel):
    similarity: float
    distance: float
    probability: float
    interpretation: str
    text: str
    image_width: int
    image_height: int
    embedding_dim: int

