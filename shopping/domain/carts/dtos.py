from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field


class BatchItemDTO(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    item_uid: str = Field(..., alias="itemUID")
    quantity: Optional[float] = None
    unit: Optional[str] = None


class CartItemDTO(BatchItemDTO):
    batch_uid: str = Field(None, alias="batchUID")


class BatchDTO(BaseModel):
    uid: str
    name: str
    type: str
    scale: int

class CartItemsBatchDTO(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    batch_uid: str = Field(..., alias="batchUID")
    name: str
    type: str
    scale: int
    items: List[BatchItemDTO]


class CartDTO(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    
    items: List[BatchItemDTO]
