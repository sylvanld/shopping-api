from fastapi import APIRouter

from shopping.core.dtos import PaginatedList
from shopping.domain.carts.dtos import CartDetailsDTO, CartReadDTO, CartWriteDTO
from shopping.domain.carts.service import CartService

router = APIRouter(tags=["carts"])
cart_service = CartService()


@router.get("/carts", response_model=PaginatedList[CartReadDTO])
async def search_carts():
    return PaginatedList(items=cart_service.search_carts())


@router.post("/carts", response_model=CartReadDTO)
async def create_cart(cart_create_dto: CartWriteDTO):
    return cart_service.create_cart(cart_create_dto)


@router.get("/carts/{cart_uuid}", response_model=CartDetailsDTO)
async def get_cart_details(cart_uuid: str):
    return cart_service.get_cart_by_uuid(cart_uuid)
