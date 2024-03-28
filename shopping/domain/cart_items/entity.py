from sqlalchemy import Column, Float, Integer, String

from shopping.extensions.database import Entity


class CartItemEntity(Entity):
    __tablename__ = "cart_items"

    id = Column(Integer, primary_key=True)
    uid = Column(String(32), unique=True)
    group_uid = Column(String(32), nullable=False)
    item_uid = Column(String(32), nullable=False)
    unit = Column(String(10), nullable=True)
    quantity = Column(Float, nullable=True)
