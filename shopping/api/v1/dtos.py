from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field


class BaseDTO(BaseModel):
    model_config = ConfigDict(populate_by_name=True)


class ChecklistBatchItemDTO(BaseDTO):
    item_uid: str = Field(..., alias="itemUID")
    quantity: Optional[float] = None
    unit: Optional[str] = None


class CartItemAddDTO(ChecklistBatchItemDTO):
    ...


class CartItemReadDTO(BaseDTO):
    item_uid: str = Field(..., alias="itemUID")
    total_quantity: Optional[float] = Field(None, alias="totalQuantity")
    remaining_quantity: Optional[float] = Field(None, alias="remainingQuantity")
    unit: Optional[str] = None
    checked: bool = False


class ChecklistItemDTO(ChecklistBatchItemDTO):
    batch_uid: str = Field(None, alias="batchUID")


class ChecklistBatchDTO(BaseDTO):
    uid: str
    name: str
    type: str
    scale: Optional[int] = Field(None, gt=0)


class ChecklistBatchWithItemsDTO(BaseDTO):
    uid: str = Field(..., alias="batchUID")
    name: str
    type: str
    scale: Optional[int] = Field(None, gt=0)
    items: List[ChecklistBatchItemDTO]


class ChecklistBatchUpdateDTO(BaseDTO):
    name: str
    scale: Optional[int] = Field(None, gt=0)


class CartDTO(BaseDTO):
    items: List[CartItemReadDTO]
