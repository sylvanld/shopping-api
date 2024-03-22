from shopping.domain.checklist_batches.entity import ChecklistBatchEntity
from shopping.domain.checklist_batches.exceptions import BatchNotFound
from shopping.extensions.database import Repository


class ChecklistBatchRepository(Repository):
    def get_by_uid(self, group_uid: str, batch_uid: str):
        """Get a batch of items by UID.

        Raises:
            BatchNotFound: If no batch exists with this UID within provided group.
        """
        batch = self.query(group_uid, batch_uid).first()
        if batch is None:
            raise BatchNotFound(f"No batch with UID {batch_uid} in group {group_uid}")
        return batch

    def query(self, group_uid: str, batch_uid: str = None):
        filters = [ChecklistBatchEntity.group_uid == group_uid]
        if batch_uid:
            filters.append(ChecklistBatchEntity.uid == batch_uid)
        return self.session.query(ChecklistBatchEntity).filter(*filters)

    def exists(self, group_uid: str, batch_uid: str):
        return self.query(group_uid, batch_uid=batch_uid).count() > 0
