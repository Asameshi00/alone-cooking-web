# !/usr/bin/env python
# -*- coding: utf-8 -*-


from pydantic import BaseModel, Field

class RakutenRecipeSearchResponse(BaseModel):
    """
    楽天レシピAPIを使用してレシピを検索して返ってくるレスポンスのスキーマ

    Args:
        BaseModel (_type_): 基底クラス
    """
    recipe_id: str # レシピID
    title: str # レシピのタイトル
    description: str # レシピの説明
    url: str # レシピのURL
    image_url: str | None = None # レシピの画像URL
    materials: list[str] = Field(default_factory=list) # レシピの材料


class YouTubeVideoResponse(BaseModel):
    """
    YouTube動画1件のレスポンスのスキーマ

    Args:
        BaseModel (_type_): 基底クラス
    """
    video_id: str # 動画ID
    title: str # 動画タイトル
    description: str # 動画の説明
    url: str # 動画URL
    thumbnail_url: str | None = None # サムネイルURL


class RecipeSearchResult(BaseModel):
    """
    統合した検索結果のスキーマ

    Args:
        BaseModel (_type_): 基底クラス
    """
    ingredient: str # 検索した食材名
    rakuten_recipes: list[RakutenRecipeSearchResponse] # 楽天レシピ検索結果
    youtube_videos: list[YouTubeVideoResponse] # YouTube動画検索結果
