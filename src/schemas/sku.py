from pydantic import BaseModel, ConfigDict
from uuid import UUID
from typing import List, Optional


class SKUCharacteristic(BaseModel):
    name: str
    value: str


class SKUPublicResponse(BaseModel):
    id: UUID
    name: str
    price: int
    discount: int
    image: Optional[str] = None
    active_quantity: int
    characteristics: List[SKUCharacteristic] = []

    model_config = ConfigDict(from_attributes=True)

    @property
    def in_stock(self) -> bool:
        return self.active_quantity > 0