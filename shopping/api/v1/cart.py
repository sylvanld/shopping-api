from fastapi import APIRouter, Path

from shopping.api.v1.dtos import CartDTO
from shopping.service.cart import CartService

router = APIRouter(tags=["cart"])
cart_service = CartService()


@router.get("/groups/{groupUID}/cart", response_model=CartDTO)
async def get_cart_details(group_uid: str = Path(..., alias="groupUID")):
    return cart_service.get_cart(group_uid)
