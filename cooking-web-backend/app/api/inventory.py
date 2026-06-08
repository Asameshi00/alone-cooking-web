# !/usr/bin/env python
# -*- coding: utf-8 -*-


from fastapi import APIRouter, Query
from app.schemas.inventory import InventoryCreate, InventoryResponse
from app.services.inventory.inventory_service import InventoryService

inventory_service = InventoryService()

router = APIRouter(prefix="/inventory", tags=["inventory"])

# 在庫を取得するエンドポイント
@router.get("", response_model=list[InventoryResponse])
async def list_inventory(user_id: int = Query(..., ge=1)) -> list[InventoryResponse]:
    return [InventoryResponse.model_validate(item) for item in inventory_service.list_inventory(user_id)]


# 食材を在庫に追加するエンドポイント
@router.post("", response_model=InventoryResponse)
async def add_inventory(payload: InventoryCreate) -> InventoryResponse:
    item = inventory_service.add_inventory(payload.user_id, payload.ingredient_name, payload.quantity, payload.unit)
    return InventoryResponse.model_validate(item)


# 在庫を削除するエンドポイント
@router.delete("/{inventory_id}", status_code=204)
async def delete_inventory(inventory_id: int) -> None:
    inventory_service.delete_inventory(inventory_id)
