# !/usr/bin/env python
# -*- coding: utf-8 -*-


from fastapi import APIRouter, Query

from app.schemas.recipe import RecipeSearchResult
from app.services.rakuten import RakutenRecipeService

router = APIRouter(prefix="/recipes", tags=["recipes"])
service = RakutenRecipeService()

# レシピを検索するエンドポイント
@router.get("/search", response_model=RecipeSearchResult)
async def search_recipe(
    ingredient: str = Query(..., min_length=1, description="検索したい食材名"),
    limit: int = Query(10, ge=1, le=30),
) -> RecipeSearchResult:
    items = await service.search(ingredient=ingredient, limit=limit)
    return RecipeSearchResult(source="rakuten", total=len(items), items=items)
