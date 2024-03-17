from collections import defaultdict
from dataclasses import dataclass
from typing import List
from uuid import uuid4

from shopping.domain.carts.dtos import CartItemsBatchDTO
from shopping.domain.carts.exceptions import BatchAlreadyExists
from shopping.extensions.database import session

from .entity import CartBatchEntity, CartItemEntity
from sqlalchemy.orm import Session

class Repository:
    def __init__(self, session: Session):
        self.session = session
        
    def add(self, entity):
        self.session.add(entity)

    def commit(self):
        self.session.commit()


class BatchRepository(Repository):
    def query(self, group_uid: str, batch_uid: str = None):
        filters = [CartBatchEntity.group_uid == group_uid]
        if batch_uid:
            filters.append(CartBatchEntity.uid == batch_uid)
        return self.session.query(CartBatchEntity).filter(*filters)
    
    def exists(self, group_uid: str, batch_uid: str):
        return self.query(group_uid, batch_uid=batch_uid).count() > 0


def aggregate_items(items: List[CartItemEntity]) -> List[CartItemEntity]:   
    aggregated_items_index = {}
    aggregated_items = []
        
    for item in items:
        aggregated_item = aggregated_items_index.get((item.item_uid, item.unit))
        if aggregated_item is None:
            aggregated_item = CartItemEntity(
                item_uid = item.item_uid,
                unit = item.unit,
                quantity = item.quantity
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
    items: List[CartBatchEntity]


class CartItemRepository(Repository):
    def query(self, group_uid: str, batch_uid: str = None):
        filters = [CartItemEntity.group_uid == group_uid]
        if batch_uid:
            filters.append(CartItemEntity.batch_uid == batch_uid)
        return self.session.query(CartItemEntity).filter(*filters)


class CartService:
    def __init__(self):
        self.batch_repository = BatchRepository(session)
        self.cart_item_repository = CartItemRepository(session)
        
    def get_cart(self, group_uid: str) -> Cart:
        items = self.cart_item_repository.query(group_uid=group_uid).all()
        return Cart(items=aggregate_items(items))

    def get_cart_items(self, group_uid: str):
        query = self.cart_item_repository.query(group_uid=group_uid)
        return query.all()

    def get_cart_items_by_batch(self, group_uid: str):
        items = self.get_cart_items(group_uid)
        items_by_batch = defaultdict(list)
        for item in items:
            items_by_batch[item.batch_uid].append(item)
        return [{"batch_uid": batch_uid, "items": items} for batch_uid, items in items_by_batch.items()]
    
    def get_batches(self, group_uid: str):
        return self.batch_repository.query(group_uid).all()

    def add_cart_items_batch(self, group_uid: str, items_batch_dto: CartItemsBatchDTO):
        if self.batch_repository.exists(group_uid, items_batch_dto.batch_uid):
            raise BatchAlreadyExists("Batch already exists: %s" % items_batch_dto.batch_uid)

        batch = CartBatchEntity(
            uid=items_batch_dto.batch_uid,
            group_uid=group_uid,
            name=items_batch_dto.name,
            type=items_batch_dto.type,
            scale=items_batch_dto.scale,
            base_scale=items_batch_dto.scale,
        )
        self.batch_repository.add(batch)

        for item_dto in items_batch_dto.items:
            item = CartItemEntity(
                uid=uuid4().hex,
                group_uid=group_uid,
                item_uid=item_dto.item_uid,
                batch_uid=items_batch_dto.batch_uid,
                unit=item_dto.unit,
                quantity=item_dto.quantity,
            )
            self.cart_item_repository.add(item)

        session.commit()
