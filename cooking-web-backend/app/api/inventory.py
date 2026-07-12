# !/usr/bin/env python
# -*- coding: utf-8 -*-


from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import db_session_dep
from app.schemas.inventory import InventoryCreate, InventoryResponse
from app.services.inventory_service import InventoryService

inventory_service = InventoryService()
router = APIRouter(prefix="/inventory", tags=["inventory"])


# 在庫を取得するエンドポイント
@router.get("", response_model=list[InventoryResponse])
async def list_inventory(
    user_id: int = Query(..., ge=1),
    session: AsyncSession = Depends(db_session_dep),
) -> list[InventoryResponse]:
    items = await inventory_service.list_inventory(session=session, user_id=user_id)
    return [InventoryResponse.model_validate(item) for item in items]


# 食材を在庫に追加するエンドポイント
@router.post("", response_model=InventoryResponse)
async def add_inventory(
    payload: InventoryCreate,
    session: AsyncSession = Depends(db_session_dep),
) -> InventoryResponse:
    item = await inventory_service.add_inventory(
        session=session,
        user_id=payload.user_id,
        ingredient_name=payload.ingredient_name,
        quantity=payload.quantity,
        unit=payload.unit,
    )
    return InventoryResponse.model_validate(item)


# 在庫を削除するエンドポイント
@router.delete("/{inventory_id}", status_code=204)
async def delete_inventory(
    inventory_id: int,
    session: AsyncSession = Depends(db_session_dep),
) -> None:
    try:
        await inventory_service.delete_inventory(session=session, inventory_id=inventory_id)
    except ValueError:
        raise HTTPException(status_code=404, detail="在庫が見つかりません")
