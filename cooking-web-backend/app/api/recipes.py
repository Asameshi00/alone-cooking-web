# !/usr/bin/env python
# -*- coding: utf-8 -*-

import asyncio

from fastapi import APIRouter, Query

from app.schemas.recipe import CombinedRecipeSearchResult, RecipeSearchRequest
from app.services.rakuten import RakutenRecipeService
from app.services.youtube import YouTubeRecipeService

router = APIRouter(prefix="/recipes", tags=["recipes"])
rakuten_service = RakutenRecipeService()
youtube_service = YouTubeRecipeService()


async def _search(ingredient: str, limit: int) -> CombinedRecipeSearchResult:
    rakuten_recipes, youtube_videos = await asyncio.gather(
        rakuten_service.search(ingredient=ingredient, limit=limit),
        youtube_service.search(ingredient=ingredient, limit=limit),
    )
    return CombinedRecipeSearchResult(
        ingredient=ingredient,
        rakuten_recipes=rakuten_recipes,
        youtube_videos=youtube_videos,
    )


# GETエンドポイント: クエリパラメータで食材を指定してレシピを検索する
@router.get("/search", response_model=CombinedRecipeSearchResult)
async def search_recipe_get(
    ingredient: str = Query(..., min_length=1, description="検索したい食材名"),
    limit: int = Query(10, ge=1, le=30),
) -> CombinedRecipeSearchResult:
    return await _search(ingredient=ingredient, limit=limit)


# POSTエンドポイント: リクエストボディで食材を指定してレシピを検索する
@router.post("/search", response_model=CombinedRecipeSearchResult)
async def search_recipe_post(
    payload: RecipeSearchRequest,
) -> CombinedRecipeSearchResult:
    return await _search(ingredient=payload.ingredient, limit=payload.limit)
