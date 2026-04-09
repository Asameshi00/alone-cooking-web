from fastapi import APIRouter, Depends, Query
from sqlalchemy import Select, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import db_session_dep
from app.models.inventory import InventoryItem
from app.schemas.inventory import InventoryCreate, InventoryResponse

router = APIRouter(prefix="/inventory", tags=["inventory"])


@router.get("", response_model=list[InventoryResponse])
async def list_inventory(
    user_id: int = Query(..., ge=1),
    session: AsyncSession = Depends(db_session_dep),
) -> list[InventoryResponse]:
    stmt: Select[tuple[InventoryItem]] = select(InventoryItem).where(InventoryItem.user_id == user_id)
    rows = (await session.execute(stmt)).scalars().all()
    return [InventoryResponse.model_validate(row) for row in rows]


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
