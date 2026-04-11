# !/usr/bin/env python
# -*- coding: utf-8 -*-


from datetime import datetime
from pydantic import BaseModel, Field
from app.schemas.common import ORMBase

# 在庫を作成するリクエスト
class InventoryCreate(BaseModel):
    user_id: int = Field(..., ge=1)
    ingredient_name: str = Field(..., min_length=1, max_length=120)
    quantity: int = Field(default=1, ge=1)
    unit: str = Field(default="個", min_length=1, max_length=30)

# 在庫を取得するレスポンス
class InventoryResponse(ORMBase):
    id: int
    user_id: int
    ingredient_name: str
    quantity: int
    unit: str
    created_at: datetime
