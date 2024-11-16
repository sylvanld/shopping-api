from typing import List

from fastapi import APIRouter, Path

from shopping.api.v1.dtos import CartDTO, CartItemAddDTO, CartItemQuantityDTO, CartItemReadDTO
from shopping.service.cart import CartService

router = APIRouter(tags=["cart"])
cart_service = CartService()


@router.get("/groups/{groupUID}/cart", response_model=CartDTO)
async def get_cart_details(group_uid: str = Path(..., alias="groupUID")):
    return cart_service.get_cart(group_uid)


@router.post("/groups/{groupUID}/cart/empty")
async def empty_cart(group_uid: str = Path(..., alias="groupUID")):
    return cart_service.empty_cart(group_uid)


@router.post("/groups/{groupUID}/cart/items", response_model=CartItemQuantityDTO)
async def add_item_to_cart(item_dto: CartItemAddDTO, group_uid: str = Path(..., alias="groupUID")):
    return cart_service.add_cart_item(group_uid, item_dto)


@router.get("/groups/{groupUID}/cart/items", response_model=List[CartItemReadDTO])
async def get_cart_items(group_uid: str = Path(..., alias="groupUID")):
    return cart_service.get_cart_items(group_uid)


@router.delete("/groups/{groupUID}/cart/items/{cartItemUID}")
async def remove_item_from_cart(
    group_uid: str = Path(..., alias="groupUID"), cart_item_uid: str = Path(..., alias="cartItemUID")
):
    return cart_service.remove_cart_item(group_uid, cart_item_uid)
