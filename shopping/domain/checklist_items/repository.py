from shopping.domain.checklist_items.entity import ChecklistItemEntity
from shopping.extensions.database import Repository


class ChecklistItemRepository(Repository):
    def query(self, group_uid: str, batch_uid: str = None):
        filters = [ChecklistItemEntity.group_uid == group_uid]
        if batch_uid:
            filters.append(ChecklistItemEntity.batch_uid == batch_uid)
        return self.session.query(ChecklistItemEntity).filter(*filters)
