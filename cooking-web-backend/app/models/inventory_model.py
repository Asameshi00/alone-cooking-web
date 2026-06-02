# !/usr/bin/env python
# -*- coding: utf-8 -*-


from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

# 在庫モデル
class InventoryItem(Base):
    # テーブル名
    __tablename__ = "inventory_items"

    # 主キー
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    # ユーザーID
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    # 食材名
    ingredient_name: Mapped[str] = mapped_column(String(120), nullable=False, index=True)
    # 数量
    quantity: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    # 単位
    unit: Mapped[str] = mapped_column(String(30), nullable=False, default="個")
    # 作成日時
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)


    # ユーザーとの関係を定義
    # 在庫はユーザーに属する
    user = relationship("User", back_populates="inventories")
