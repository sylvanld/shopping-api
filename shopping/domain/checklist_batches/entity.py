from sqlalchemy import Column, Integer, String, UniqueConstraint

from shopping.extensions.database import Entity


class ChecklistBatchEntity(Entity):
    __tablename__ = "checklist_batches"

    __table_args__ = (UniqueConstraint("uid", "group_uid", name="_group_batch_uc"),)

    id = Column(Integer, primary_key=True)
    uid = Column(String(32), nullable=False)
    group_uid = Column(String(32), nullable=False)
    name = Column(String(40), nullable=False)
    type = Column(String(10), nullable=False)
    scale = Column(Integer, nullable=False)
    base_scale = Column(Integer, nullable=False)
