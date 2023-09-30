from datetime import datetime
from typing import List

from pydantic import BaseModel

from shopping.domain.items.dtos import ItemReadDTO


class CartWriteDTO(BaseModel):
    label: str


class CartReadDTO(BaseModel):
    uuid: str
    label: str
    creation_date: datetime


class CartDetailsDTO(CartReadDTO):
    items: List[ItemReadDTO]
