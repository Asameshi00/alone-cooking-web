# !/usr/bin/env python
# -*- coding: utf-8 -*-


from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import Select, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import db_session_dep
from app.models.inventory_model import InventoryItem
from app.schemas.inventory import InventoryCreate, InventoryResponse

router = APIRouter(prefix="/inventory", tags=["inventory"])

# 在庫を取得するエンドポイント
@router.get("", response_model=list[InventoryResponse])
async def list_inventory(
    user_id: int = Query(..., ge=1),
    session: AsyncSession = Depends(db_session_dep),
) -> list[InventoryResponse]:
    stmt: Select[tuple[InventoryItem]] = select(InventoryItem).where(InventoryItem.user_id == user_id)
    rows = (await session.execute(stmt)).scalars().all()
    return [InventoryResponse.model_validate(row) for row in rows]


# 在庫を作成するエンドポイント
@router.post("", response_model=InventoryResponse)
async def create_inventory(
    payload: InventoryCreate,
    session: AsyncSession = Depends(db_session_dep),
) -> InventoryResponse:
    item = InventoryItem(**payload.model_dump())
    session.add(item)
    await session.commit()
    await session.refresh(item)
    return InventoryResponse.model_validate(item)


# 在庫を削除するエンドポイント
@router.delete("/{item_id}", status_code=204)
async def delete_inventory(
    item_id: int,
    session: AsyncSession = Depends(db_session_dep),
) -> None:
    item = await session.get(InventoryItem, item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="指定された在庫が見つかりません")
    await session.delete(item)
    await session.commit()
