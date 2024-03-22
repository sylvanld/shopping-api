from dataclasses import dataclass
from typing import List

from shopping.domain.checklist_batches.repository import ChecklistBatchRepository
from shopping.domain.checklist_items.repository import ChecklistItemEntity, ChecklistItemRepository


def aggregate_items(items: List[ChecklistItemEntity]) -> List[ChecklistItemEntity]:
    aggregated_items_index = {}
    aggregated_items = []

    for item in items:
        aggregated_item = aggregated_items_index.get((item.item_uid, item.unit))
        if aggregated_item is None:
            aggregated_item = ChecklistItemEntity(
                item_uid=item.item_uid,
                unit=item.unit,
            )
            aggregated_items_index[(item.item_uid, item.unit)] = aggregated_item
            aggregated_items.append(aggregated_item)

        if item.quantity is not None:
            if aggregated_item.quantity is None:
                aggregated_item.quantity = item.quantity
            else:
                aggregated_item.quantity += item.quantity

    return aggregated_items


@dataclass
class Cart:
    items: List[ChecklistItemEntity]


class CartService:
    def __init__(self):
        self.checklist_batch_repository = ChecklistBatchRepository()
        self.checklist_item_repository = ChecklistItemRepository()

    def get_cart(self, group_uid: str) -> Cart:
        """Get cart statistics and aggregated items."""
        items = self.get_checklist_items(group_uid)
        return Cart(items=aggregate_items(items))

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
