# !/usr/bin/env python
# -*- coding: utf-8 -*-


from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field
from app.schemas.common import ORMBase

# お気に入りの種類
class FavoriteKind(str, Enum):
    RECIPE = "recipe"
    VIDEO = "video"

# お気に入りを作成するリクエスト
class FavoriteRequest(BaseModel):
    user_id: int = Field(..., ge=1) # ユーザーID
    kind: FavoriteKind # お気に入りの種類（レシピ or 動画）
    item_id: str = Field(..., min_length=1, max_length=50) # レシピID or 動画ID
    title: str = Field(..., min_length=1, max_length=255) # タイトル
    description: str | None = Field(default=None, max_length=1000) # 説明
    url: str = Field(..., min_length=1, max_length=500) # URL
    image_url: str | None = Field(default=None, max_length=500) # 画像URL

# お気に入りを取得するレスポンス
class FavoriteResponse(ORMBase):
    id: int # お気に入りID
    user_id: int # ユーザーID
    kind: FavoriteKind # お気に入りの種類（レシピ or 動画）
    item_id: str # レシピID or 動画ID
    title: str # タイトル
    description: str | None # 説明
    url: str # URL
    image_url: str | None # 画像URL
    created_at: datetime # 作成日時
