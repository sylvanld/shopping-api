from typing import List

from fastapi import APIRouter, Path

from shopping.api.v1.dtos import CartDTO, CartItemAddDTO
from shopping.service.cart import CartService

router = APIRouter(tags=["cart"])
cart_service = CartService()


@router.get("/groups/{groupUID}/cart", response_model=CartDTO)
async def get_cart_details(group_uid: str = Path(..., alias="groupUID")):
    return cart_service.get_cart(group_uid)


@router.post("/groups/{groupUID}/cart/items")
async def add_item_to_cart(item_dto: CartItemAddDTO, group_uid: str = Path(..., alias="groupUID")):
    return cart_service.add_cart_item(group_uid, item_dto)


@router.get("/groups/{groupUID}/cart/items", response_model=List[CartItemAddDTO])
async def get_cart_items(group_uid: str = Path(..., alias="groupUID")):
    return cart_service.get_cart_items(group_uid)
