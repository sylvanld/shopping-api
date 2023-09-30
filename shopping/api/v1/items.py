from fastapi import APIRouter

from shopping.domain.carts.service import CartService
from shopping.domain.items.service import ItemService

router = APIRouter(tags=["items"])
cart_service = CartService()
item_service = ItemService()


@router.post("/carts/{cart_uuid}/items")
async def add_cart_item(cart_uuid: str):
    cart = cart_service.get_cart_by_uuid(cart_uuid)
    item_service.add_cart_item(cart)
