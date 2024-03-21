from typing import List

from fastapi import APIRouter, HTTPException, Path, status

from shopping.domain.carts.dtos import BatchDTO, CartBatchUpdateDTO, CartDTO, CartItemDTO, CartItemsBatchDTO
from shopping.domain.carts.exceptions import BatchAlreadyExists, BatchNotFound
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


@router.put("/groups/{groupUID}/cart/batch/{batchUID}", response_model=BatchDTO)
async def update_batch(
    batch_update_dto: CartBatchUpdateDTO,
    group_uid: str = Path(..., alias="groupUID"),
    batch_uid: str = Path(..., alias="batchUID"),
):
    try:
        return cart_service.update_cart_batch(group_uid, batch_uid, batch_update_dto)
    except BatchNotFound as error:
        raise HTTPException(404, detail=str(error))


@router.delete("/groups/{groupUID}/cart/batch/{batchUID}")
async def delete_batch(group_uid: str = Path(..., alias="groupUID"), batch_uid: str = Path(..., alias="batchUID")):
    try:
        return cart_service.delete_cart_batch(group_uid, batch_uid)
    except BatchNotFound as error:
        raise HTTPException(404, detail=str(error))
