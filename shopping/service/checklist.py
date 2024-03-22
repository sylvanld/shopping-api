from uuid import uuid4

from shopping.api.v1.dtos import ChecklistBatchUpdateDTO, ChecklistBatchWithItemsDTO
from shopping.domain.checklist_batches.exceptions import BatchAlreadyExists
from shopping.domain.checklist_batches.repository import ChecklistBatchEntity, ChecklistBatchRepository
from shopping.domain.checklist_items.repository import ChecklistItemEntity, ChecklistItemRepository


class ChecklistService:
    def __init__(self):
        self.checklist_batch_repository = ChecklistBatchRepository()
        self.checklist_item_repository = ChecklistItemRepository()

    def get_checklist_batches(self, group_uid: str):
        return self.checklist_batch_repository.query(group_uid).all()

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

    def add_batch_to_checklist(self, group_uid: str, batch_dto: ChecklistBatchWithItemsDTO):
        """Add a batch of items to group's checklist."""
        if self.checklist_batch_repository.exists(group_uid, batch_dto.uid):
            raise BatchAlreadyExists("Batch already exists: %s" % batch_dto.uid)

        batch = ChecklistBatchEntity(
            uid=batch_dto.uid,
            group_uid=group_uid,
            name=batch_dto.name,
            type=batch_dto.type,
            scale=batch_dto.scale,
            base_scale=batch_dto.scale,
        )
        self.checklist_batch_repository.add(batch)

        for item_dto in batch_dto.items:
            item = ChecklistItemEntity(
                uid=uuid4().hex,
                group_uid=group_uid,
                item_uid=item_dto.item_uid,
                batch_uid=batch_dto.uid,
                unit=item_dto.unit,
                quantity=item_dto.quantity,
            )
            self.checklist_item_repository.add(item)

        self.checklist_batch_repository.commit()
        self.checklist_item_repository.commit()

    def update_checklist_batch(self, group_uid: str, batch_uid: str, batch_dto: ChecklistBatchUpdateDTO):
        """Update properties of a batch of items.

        Raises:
            BatchNotFound: If no batch exists with this UID within provided group.
        """
        batch = self.checklist_batch_repository.get_by_uid(group_uid, batch_uid)

        batch.name = batch_dto.name
        batch.scale = batch_dto.scale
        self.checklist_batch_repository.commit()

        return batch

    def delete_checklist_batch(self, group_uid: str, batch_uid: str):
        """Delete a batch and associated items from checklist.

        Raises:
            BatchNotFound: If no batch exists with this UID within provided group.
        """
        items = self.checklist_item_repository.query(group_uid, batch_uid)
        for item in items:
            self.checklist_item_repository.delete(item)

        batch = self.checklist_batch_repository.get_by_uid(group_uid, batch_uid)
        self.checklist_batch_repository.delete(batch)
        self.checklist_batch_repository.commit()
