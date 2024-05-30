from pydantic import BaseModel, HttpUrl, validator
from typing import List

class TextImagePair(BaseModel):
    product_image_url: List[HttpUrl]
    product_title: str

class EmbeddingRequest(BaseModel):
    pairs: List[TextImagePair]

    @validator('pairs')
    def pairs_must_not_be_empty(cls, v):
        if not v:
            raise ValueError('pairs must not be empty')
        return v
