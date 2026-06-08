# !/usr/bin/env python
# -*- coding: utf-8 -*-


from app.services.logger import get_logger
from app.core.config import get_settings

from app.models.inventory_model import InventoryItem
from app.schemas.inventory import InventoryCreate, InventoryResponse


class InventoryService:
    """ 在庫サービス """

    def __init__(self) -> None:
        """ コンストラクタ """
        self.logger = get_logger(__name__)
        self.settings = get_settings()

    def add_inventory(self, user_id: int, ingredient_name: str, quantity: int, unit: str) -> None:
        """
        食材を在庫に追加する
        """
        item = InventoryItem(
            user_id=user_id,
            ingredient_name=ingredient_name,
            quantity=quantity,
            unit=unit
        )
        self.logger.info(f"食材を在庫に追加しました: user_id={user_id}, ingredient_name={ingredient_name}, quantity={quantity}, unit={unit}")
        item.save()
        return item


    def list_inventory(self, user_id: int) -> list[InventoryItem]:
        """
        在庫を取得する
        """
        items = InventoryItem.objects.filter(user_id=user_id)
        self.logger.info(f"在庫を取得しました: user_id={user_id}, items={items}")
        return items


    def delete_inventory(self, inventory_id: int) -> None:
        """
        在庫を削除する
        """
        item = InventoryItem.objects.get(id=inventory_id)
        if item is None:
            raise ValueError(f"在庫が見つかりません: inventory_id={inventory_id}")
        self.logger.info(f"在庫を削除しました: inventory_id={inventory_id}")
        item.delete()
