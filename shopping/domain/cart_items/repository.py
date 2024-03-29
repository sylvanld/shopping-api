from uuid import uuid4

from shopping.core.types import UNDEFINED
from shopping.domain.cart_items.entity import CartItemEntity
from shopping.extensions.database import Repository


class CartItemRepository(Repository):
    def query(self, group_uid: str, item_uid: str = UNDEFINED, unit: str = UNDEFINED, cart_item_uid: str = UNDEFINED):
        filters = [CartItemEntity.group_uid == group_uid]
        if item_uid != UNDEFINED:
            filters.append(CartItemEntity.item_uid == item_uid)
        if unit != UNDEFINED:
            filters.append(CartItemEntity.unit == unit)
        if cart_item_uid != UNDEFINED:
            filters.append(CartItemEntity.uid == cart_item_uid)
        return self.session.query(CartItemEntity).filter(*filters)

    def get(self, group_uid: str, item_uid: str, unit: str):
        item = self.query(group_uid, item_uid=item_uid, unit=unit).first()
        if item is None:
            item = CartItemEntity(uid=uuid4().hex, group_uid=group_uid, item_uid=item_uid, unit=unit)
            self.session.add(item)
        return item
