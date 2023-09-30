from sqlalchemy import Column, ForeignKey, Integer, String

from shopping.extensions.database import Entity


class ItemEntity(Entity):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True)
    cart_id = Column(ForeignKey("carts.id"), nullable=False)
    uuid = Column(String(32), unique=True)
