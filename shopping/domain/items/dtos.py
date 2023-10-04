from pydantic import BaseModel


class ItemReadDTO(BaseModel):
    uuid: str


class ItemWriteDTO(BaseModel):
    label: str
    quantity: str = None
    unit: str = None
