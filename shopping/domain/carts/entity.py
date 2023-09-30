from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.orm import relationship

from shopping.extensions.database import Entity


class CartEntity(Entity):
    __tablename__ = "carts"

    id = Column(Integer, primary_key=True)
    uuid = Column(String(32), unique=True)
    label = Column(String, nullable=False)
    creation_date = Column(DateTime, default=datetime.utcnow)

    items = relationship("ItemEntity")
