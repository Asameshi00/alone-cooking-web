# !/usr/bin/env python
# -*- coding: utf-8 -*-


from datetime import datetime
from pydantic import BaseModel, Field
from app.schemas.common import ORMBase

# 在庫のスキーマ
class InventoryCreate(BaseModel):
    user_id: int = Field(..., ge=1) # ユーザーID
    ingredient_name: str = Field(..., min_length=1, max_length=120) # 食材名
    quantity: int = Field(default=1, ge=1) # 数量
    unit: str = Field(default="個", min_length=1, max_length=30) # 単位

# 在庫を取得するレスポンス
class InventoryResponse(ORMBase):
    id: int # 在庫ID
    user_id: int # ユーザーID
    ingredient_name: str # 食材名
    quantity: int # 数量
    unit: str # 単位
    created_at: datetime # 作成日時
