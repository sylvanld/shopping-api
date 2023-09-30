from uuid import uuid4

from shopping.domain.carts.dtos import CartWriteDTO
from shopping.extensions.database import session

from .entity import CartEntity


class CartRepository:
    def __init__(self):
        self.session = session

    def get_by_uuid(self, uuid: str):
        return self.session.query(CartEntity).filter_by(uuid=uuid).first()

    def search(self):
        query = self.session.query(CartEntity)
        return query.all()

    def create(self, cart_create_dto: CartWriteDTO):
        cart = CartEntity(uuid=uuid4().hex)
        self.session.add(cart)
        self.update(cart, cart_create_dto)
        return cart

    def update(self, cart: CartEntity, cart_update_dto: CartWriteDTO):
        cart.label = cart_update_dto.label
        self.session.commit()


class CartService:
    def __init__(self):
        self.cart_repository = CartRepository()

    def get_cart_by_uuid(self, cart_uuid: str):
        return self.cart_repository.get_by_uuid(cart_uuid)

    def search_carts(self):
        return self.cart_repository.search()

    def create_cart(self, cart_create_dto: CartWriteDTO):
        return self.cart_repository.create(cart_create_dto)
