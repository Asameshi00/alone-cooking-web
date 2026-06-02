# !/usr/bin/env python
# -*- coding: utf-8 -*-

import asyncio

from fastapi import APIRouter, Query

from app.schemas.recipe import RecipeSearchResult
from app.services.rakuten_service import RakutenRecipeService
from app.services.youtube_service import YouTubeRecipeService

router = APIRouter(prefix="/recipes", tags=["recipes"])
rakuten_service = RakutenRecipeService()
youtube_service = YouTubeRecipeService()


# TODO: _searchメソッドをserviceに移動する
async def _search_recipes(ingredient: str, limit: int) -> RecipeSearchResult:
    """
    食材から限られた件数レシピ検索をする
    Args:
        ingredient (str): 食材
        limit (int): 件数の絞り込み数

    Returns:
        CombinedRecipeSearchResult: 検索結果
    """
    rakuten_recipes, youtube_videos = await asyncio.gather(
        rakuten_service.search_for_recipes(ingredient=ingredient, limit=limit),
        youtube_service.search_for_recipes(ingredient=ingredient, limit=limit),
    )

    return RecipeSearchResult(
        ingredient=ingredient,
        rakuten_recipes=rakuten_recipes,
        youtube_videos=youtube_videos,
    )


# GETエンドポイント: クエリパラメータで食材を指定してレシピを検索する
@router.get("/search", response_model=RecipeSearchResult)
async def search_recipes(
    ingredient: str = Query(..., min_length=1, description="検索したい食材名"),
    limit: int = Query(10, ge=1, le=30),
) -> RecipeSearchResult:
    return await _search_recipes(ingredient=ingredient, limit=limit)
