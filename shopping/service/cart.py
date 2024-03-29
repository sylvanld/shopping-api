from dataclasses import dataclass
from typing import List, Optional

from shopping.api.v1.dtos import ChecklistBatchItemDTO
from shopping.domain.cart_items.exceptions import CartItemNotFound
from shopping.domain.cart_items.repository import CartItemRepository
from shopping.domain.checklist_batches.repository import ChecklistBatchRepository
from shopping.domain.checklist_items.repository import ChecklistItemEntity, ChecklistItemRepository


@dataclass
class Cart:
    items: List[ChecklistItemEntity]


@dataclass
class CartItem:
    item_uid: str
    total_quantity: Optional[float] = None
    remaining_quantity: Optional[float] = None
    unit: str = None
    checked: bool = False
    cart_item_uid: str = None


def aggregate_items(items: List[ChecklistItemEntity]) -> List[CartItem]:
    aggregated_items_index = {}
    aggregated_items: List[CartItem] = []

    for item in items:
        aggregated_item = aggregated_items_index.get((item.item_uid, item.unit))
        if aggregated_item is None:
            aggregated_item = CartItem(
                item_uid=item.item_uid,
                unit=item.unit,
            )
            aggregated_items_index[(item.item_uid, item.unit)] = aggregated_item
            aggregated_items.append(aggregated_item)

        if item.quantity is not None:
            if aggregated_item.total_quantity is None:
                aggregated_item.total_quantity = item.quantity
            else:
                aggregated_item.total_quantity += item.quantity

    for item in aggregated_items:
        item.remaining_quantity = item.total_quantity

    return aggregated_items


class CartService:
    def __init__(self):
        self.checklist_batch_repository = ChecklistBatchRepository()
        self.checklist_item_repository = ChecklistItemRepository()
        self.cart_item_repository = CartItemRepository()

    def get_cart(self, group_uid: str) -> Cart:
        """Get cart statistics and aggregated items."""
        items = aggregate_items(self.get_checklist_items(group_uid))
        cart_items = {(item.item_uid, item.unit): item for item in self.get_cart_items(group_uid)}
        for item in items:
            item.remaining_quantity = item.total_quantity
            cart_item = cart_items.get((item.item_uid, item.unit))
            if cart_item:
                item.cart_item_uid = cart_item.uid
                if item.remaining_quantity and cart_item.quantity:
                    item.remaining_quantity -= cart_item.quantity
                if item.remaining_quantity is None or item.remaining_quantity <= 0:
                    item.checked = True
        return Cart(items=items)

    def add_cart_item(self, group_uid: str, item_dto: ChecklistBatchItemDTO):
        """Add item quantity to group's cart."""
        item = self.cart_item_repository.get(group_uid, item_dto.item_uid, item_dto.unit)
        if item_dto.quantity:
            if item.quantity is None:
                item.quantity = item_dto.quantity
            else:
                item.quantity += item_dto.quantity
        self.cart_item_repository.commit()
        return item

    def remove_cart_item(self, group_uid: str, cart_item_uid: str):
        cart_item = self.cart_item_repository.query(group_uid=group_uid, cart_item_uid=cart_item_uid).first()
        if cart_item is None:
            raise CartItemNotFound(f"No cart item with UID {cart_item_uid} in group {group_uid}")
        self.cart_item_repository.delete(cart_item)
        self.cart_item_repository.commit()

    def get_cart_items(self, group_uid: str):
        """Get items that have been added to group's cart."""
        return self.cart_item_repository.query(group_uid).all()

    def get_checklist_items(self, group_uid: str):
        """Get details of checklist items (items from different batches are not aggregated)."""
        items = self.checklist_item_repository.query(group_uid=group_uid).all()
        batch_by_uid = {
            batch_uid: self.checklist_batch_repository.get_by_uid(group_uid, batch_uid)
            for batch_uid in set(item.batch_uid for item in items)
        }
        for item in items:
            if item.batch_uid and item.quantity:
                batch = batch_by_uid[item.batch_uid]
                item.quantity = round(item.quantity * batch.scale / batch.base_scale, 2)
        return items
