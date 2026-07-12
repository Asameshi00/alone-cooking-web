# !/usr/bin/env python
# -*- coding: utf-8 -*-


from sqlalchemy import Select, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.inventory_model import InventoryItem
from app.services.logger import get_logger


class InventoryService:
    """ 在庫サービスクラス """

    def __init__(self) -> None:
        """ コンストラクタ """
        self.logger = get_logger(__name__)

    # 食材を在庫に追加する
    async def add_inventory(
        self,
        session: AsyncSession,
        user_id: int,
        ingredient_name: str,
        quantity: int,
        unit: str,
    ) -> InventoryItem:
        item = InventoryItem(
            user_id=user_id,
            ingredient_name=ingredient_name,
            quantity=quantity,
            unit=unit
        )
        session.add(item)
        await session.commit()
        await session.refresh(item)
        self.logger.info(f"食材を在庫に追加しました: user_id={user_id}, ingredient_name={ingredient_name}, quantity={quantity}, unit={unit}")
        return item


    # 在庫を取得する
    async def list_inventory(self, session: AsyncSession, user_id: int) -> list[InventoryItem]:
        stmt: Select[tuple[InventoryItem]] = select(InventoryItem).where(InventoryItem.user_id == user_id)
        items = list((await session.execute(stmt)).scalars().all())
        self.logger.info(f"在庫を取得しました: user_id={user_id}, items={items}")
        return items


    # 在庫にある食材を削除する
    async def delete_inventory(self, session: AsyncSession, inventory_id: int) -> None:
        item = await session.get(InventoryItem, inventory_id)
        if item is None:
            raise ValueError(f"在庫が見つかりません: inventory_id={inventory_id}")

        await session.delete(item)
        await session.commit()
        self.logger.info(f"在庫を削除しました: inventory_id={inventory_id}")
