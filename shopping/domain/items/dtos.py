from pydantic import BaseModel


class ItemReadDTO(BaseModel):
    uuid: str
