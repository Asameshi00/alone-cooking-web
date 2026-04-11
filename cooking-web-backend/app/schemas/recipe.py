# !/usr/bin/env python
# -*- coding: utf-8 -*-


from pydantic import BaseModel, Field

# 楽天レシピAPIを使用してレシピを検索するレスポンス
class RecipeSearchResponse(BaseModel):
    recipe_id: str # レシピID
    title: str # レシピのタイトル
    description: str # レシピの説明
    url: str # レシピのURL
    image_url: str | None = None # レシピの画像URL
    materials: list[str] = Field(default_factory=list) # レシピの材料

# 楽天レシピAPIを使用してレシピを検索する結果
class RecipeSearchResult(BaseModel):
    source: str
    total: int
    items: list[RecipeSearchResponse]
