from pydantic import BaseModel, ConfigDict
from uuid import UUID
from typing import List, Optional
from datetime import datetime
from src.schemas.sku import SKUPublicResponse


class CharacteristicResponse(BaseModel):
    name: str
    value: str


class ProductImageResponse(BaseModel):
    id: UUID
    url: str
    ordering: int


class ProductPublicResponse(BaseModel):
    id: UUID
    slug: str
    title: str
    description: str
    images: List[ProductImageResponse] = []
    status: str
    characteristics: List[CharacteristicResponse] = []
    skus: List[SKUPublicResponse] = []

    model_config = ConfigDict(from_attributes=True)