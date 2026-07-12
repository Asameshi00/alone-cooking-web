# !/usr/bin/env python
# -*- coding: utf-8 -*-


from datetime import datetime
from pydantic import BaseModel, Field
from app.schemas.common import ORMBase

# お気に入りレシピを作成するリクエスト
class FavoriteCreate(BaseModel):
    user_id: int = Field(..., ge=1) # ユーザーID
    recipe_id: str = Field(..., min_length=1, max_length=50) # レシピID
    recipe_title: str = Field(..., min_length=1, max_length=255) # レシピタイトル
    recipe_url: str = Field(..., min_length=1, max_length=500) # レシピURL
    recipe_image_url: str | None = Field(default=None, max_length=500) # レシピ画像URL

# お気に入りレシピを取得するレスポンス
class FavoriteResponse(ORMBase):
    id: int # お気に入りレシピID
    user_id: int # ユーザーID
    recipe_id: str # レシピID
    recipe_title: str # レシピタイトル
    recipe_url: str # レシピURL
    recipe_image_url: str | None # レシピ画像URL
    created_at: datetime # 作成日時
