from sqlalchemy import Column, Float, Integer, String, UniqueConstraint

from shopping.extensions.database import Entity


class CartBatchEntity(Entity):
    __tablename__ = "batch"

    __table_args__ = (UniqueConstraint("uid", "group_uid", name="_group_batch_uc"),)

    id = Column(Integer, primary_key=True)
    uid = Column(String(32), nullable=False)
    group_uid = Column(String(32), nullable=False)
    name = Column(String(40), nullable=False)
    type = Column(String(10), nullable=False)
    scale = Column(Integer, nullable=False)
    base_scale = Column(Integer, nullable=False)


class CartItemEntity(Entity):
    __tablename__ = "carts"

    id = Column(Integer, primary_key=True)
    uid = Column(String(32), unique=True)
    group_uid = Column(String(32), nullable=False)
    item_uid = Column(String(32), nullable=False)
    batch_uid = Column(String(32), nullable=True)
    unit = Column(String(10), nullable=True)
    quantity = Column(Float, nullable=True)
