# !/usr/bin/env python
# -*- coding: utf-8 -*-


from pydantic import BaseModel, Field

# inventory_ids → board（食材名一覧）変換リクエスト
class BoardIngredientsRequest(BaseModel):
    user_id: int = Field(..., ge=1)
    inventory_ids: list[int] = Field(..., min_length=1)

# board の内容（食材名一覧）レスポンス
class BoardIngredientsResponse(BaseModel):
    ingredient_names: list[str]

# board（食材名一覧）でレシピ検索するリクエスト
class BoardSearchRequest(BaseModel):
    ingredient_names: list[str] = Field(..., min_length=1)
    limit: int = Field(default=10, ge=1, le=30)
