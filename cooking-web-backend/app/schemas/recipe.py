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

# YouTube動画1件のレスポンス定義
class YouTubeVideoResponse(BaseModel):
    video_id: str # 動画ID
    title: str # 動画タイトル
    description: str # 動画の説明
    url: str # 動画URL
    thumbnail_url: str | None = None # サムネイルURL

# POST用リクエストボディ
class RecipeSearchRequest(BaseModel):
    ingredient: str = Field(..., min_length=1, description="検索したい食材名")
    limit: int = Field(10, ge=1, le=30)

# 楽天 + YouTube の統合検索結果
class CombinedRecipeSearchResult(BaseModel):
    ingredient: str # 検索した食材名
    rakuten_recipes: list[RecipeSearchResponse] # 楽天レシピ検索結果
    youtube_videos: list[YouTubeVideoResponse] # YouTube動画検索結果
