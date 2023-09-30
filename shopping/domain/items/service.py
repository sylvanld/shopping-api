from uuid import uuid4

from shopping.domain.carts.entity import CartEntity
from shopping.extensions.database import session

from .entity import ItemEntity


class ItemRepository:
    def __init__(self):
        self.session = session

    def create(self, cart_id: int):
        cart = ItemEntity(cart_id=cart_id, uuid=uuid4().hex)
        self.session.add(cart)
        self.session.commit()
        return cart


class ItemService:
    def __init__(self):
        self.cart_repository = ItemRepository()

    def add_cart_item(self, cart: CartEntity):
        return self.cart_repository.create(cart.id)
