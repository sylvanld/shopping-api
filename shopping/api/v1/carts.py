from typing import List

from fastapi import APIRouter, HTTPException, Path, status

from shopping.domain.carts.dtos import BatchDTO, CartDTO, CartItemDTO, CartItemsBatchDTO
from shopping.domain.carts.exceptions import BatchAlreadyExists
from shopping.domain.carts.service import CartService

router = APIRouter(tags=["carts"])
cart_service = CartService()


@router.get("/groups/{groupUID}/cart", response_model=CartDTO)
async def get_cart_endpoint(group_uid: str = Path(..., alias="groupUID")):   
    return cart_service.get_cart(group_uid)


@router.get("/groups/{groupUID}/cart/items", response_model=List[CartItemDTO])
async def get_cart_items(group_uid: str = Path(..., alias="groupUID")):
    return cart_service.get_cart_items(group_uid)


@router.post("/groups/{groupUID}/cart/batch")
async def add_batch_to_group_cart(items_batch_dto: CartItemsBatchDTO, group_uid: str = Path(..., alias="groupUID")):
    try:
        cart_service.add_cart_items_batch(group_uid, items_batch_dto)
    except BatchAlreadyExists as error:
        raise HTTPException(status.HTTP_409_CONFLICT, detail=str(error))


@router.get("/groups/{groupUID}/cart/batch", response_model=List[BatchDTO])
async def get_batches(group_uid: str = Path(..., alias="groupUID")):
    return cart_service.get_batches(group_uid)
