from typing import List

from fastapi import APIRouter, HTTPException, Path, status

from shopping.api.v1.dtos import (
    ChecklistBatchDTO,
    ChecklistBatchUpdateDTO,
    ChecklistBatchWithItemsDTO,
    ChecklistItemDTO,
)
from shopping.domain.checklist_batches.exceptions import BatchAlreadyExists, BatchNotFound
from shopping.service.checklist import ChecklistService

router = APIRouter(tags=["checklist"])
checklist_service = ChecklistService()


@router.get("/groups/{groupUID}/checklist/items", response_model=List[ChecklistItemDTO])
async def get_checklist_items(group_uid: str = Path(..., alias="groupUID")):
    return checklist_service.get_checklist_items(group_uid)


@router.post("/groups/{groupUID}/checklist/batch")
async def add_batch_to_group_checklist(
    batch_dto: ChecklistBatchWithItemsDTO, group_uid: str = Path(..., alias="groupUID")
):
    try:
        checklist_service.add_batch_to_checklist(group_uid, batch_dto)
    except BatchAlreadyExists as error:
        raise HTTPException(status.HTTP_409_CONFLICT, detail=str(error))


@router.get("/groups/{groupUID}/checklist/batch", response_model=List[ChecklistBatchDTO])
async def get_checklist_batches(group_uid: str = Path(..., alias="groupUID")):
    return checklist_service.get_checklist_batches(group_uid)


@router.put("/groups/{groupUID}/checklist/batch/{batchUID}", response_model=ChecklistBatchDTO)
async def update_checklist_batch(
    batch_dto: ChecklistBatchUpdateDTO,
    group_uid: str = Path(..., alias="groupUID"),
    batch_uid: str = Path(..., alias="batchUID"),
):
    try:
        return checklist_service.update_checklist_batch(group_uid, batch_uid, batch_dto)
    except BatchNotFound as error:
        raise HTTPException(404, detail=str(error))


@router.delete("/groups/{groupUID}/checklist/batch/{batchUID}")
async def delete_checklist_batch(
    group_uid: str = Path(..., alias="groupUID"), batch_uid: str = Path(..., alias="batchUID")
):
    try:
        return checklist_service.delete_checklist_batch(group_uid, batch_uid)
    except BatchNotFound as error:
        raise HTTPException(404, detail=str(error))
