from fastapi import APIRouter, HTTPException

from shopping.domain.carts.service import CartService
from shopping.domain.exceptions import EntityNotFound
from shopping.domain.items.dtos import ItemWriteDTO
from shopping.domain.items.service import ItemService

router = APIRouter(tags=["items"])
cart_service = CartService()
item_service = ItemService()


@router.post("/carts/{cart_uuid}/items")
async def add_cart_item(cart_uuid: str, cart_item_dto: ItemWriteDTO):
    try:
        cart = cart_service.get_cart_by_uuid(cart_uuid)
    except EntityNotFound as error:
        raise HTTPException(404, detail=f"No cart with UUID {cart_uuid}") from error

    item_service.add_cart_item(cart, cart_item_dto)
