# !/usr/bin/env python
# -*- coding: utf-8 -*-


from pydantic import BaseModel, Field

# 楽天レシピAPIを使用してレシピを検索して返ってくるレスポンス定義
# レシピごとのデータを定義
class RecipeSearchResponse(BaseModel):
    recipe_id: str # レシピID
    title: str # レシピのタイトル
    description: str # レシピの説明
    url: str # レシピのURL
    image_url: str | None = None # レシピの画像URL
    materials: list[str] = Field(default_factory=list) # レシピの材料

# 楽天レシピAPIを使用してレシピを検索して返ってくる結果を定義
# 検索結果全体のラッパーとして定義
class RecipeSearchResult(BaseModel):
    source: str # レシピのソース
    total: int # レシピの総数
    items: list[RecipeSearchResponse] # レシピのリスト
