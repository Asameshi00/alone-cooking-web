# !/usr/bin/env python
# -*- coding: utf-8 -*-


import httpx

from app.core.config import get_settings
from app.schemas.recipe import RecipeSearchResponse

RAKUTEN_SEARCH_URL = "https://app.rakuten.co.jp/services/api/Recipe/CategoryRanking/20170426"


# 楽天レシピAPIを使用してレシピを検索するサービス
class RakutenRecipeService:
    def __init__(self) -> None:
        # 設定を取得する
        self.settings = get_settings()

    # 楽天レシピAPIを使用してレシピをlimit件数分検索する
    async def search_recipes_with_ingredient(self, ingredient: str, limit: int = 10) -> list[RecipeSearchResponse]:
        if not self.settings.RAKUTEN_APP_ID:
            return self._fallback(ingredient, limit)

        # パラメータを作成する
        params = {
            "applicationId": self.settings.RAKUTEN_APP_ID,
            "categoryId": self.settings.RAKUTEN_CATEGORY_ID,
            "format": "json",
        }
        if self.settings.RAKUTEN_AFFILIATE_ID:
            params["affiliateId"] = self.settings.RAKUTEN_AFFILIATE_ID

        # 楽天レシピAPIを使用してレシピを検索する
        async with httpx.AsyncClient(timeout=15.0) as client:
            response = await client.get(RAKUTEN_SEARCH_URL, params=params)
            response.raise_for_status()
            payload = response.json()

        items = payload.get("result", [])[:limit]
        result: list[RecipeSearchResponse] = []
        for idx, item in enumerate(items):
            result.append(
                RecipeSearchResponse(
                    recipe_id=f"rakuten-{idx}",
                    title=item.get("recipeTitle", ""),
                    description=item.get("recipeDescription", ""),
                    url=item.get("recipeUrl", ""),
                    image_url=item.get("foodImageUrl"),
                    materials=item.get("recipeMaterial", []),
                )
            )
        return [r for r in result if ingredient in "".join([r.title, r.description, " ".join(r.materials)])] or result

    def _fallback(self, ingredient: str, limit: int) -> list[RecipeSearchResponse]:
        demo = [
            RecipeSearchResponse(
                recipe_id=f"local-{i}",
                title=f"{ingredient}の簡単レシピ {i + 1}",
                description=f"{ingredient}を使った時短メニューです。",
                url="https://example.com/recipe",
                image_url=None,
                materials=[ingredient, "塩", "こしょう"],
            )
            for i in range(limit)
        ]
        return demo
