# !/usr/bin/env python
# -*- coding: utf-8 -*-


import httpx

from app.core.config import get_settings
from app.schemas.recipe import RecipeSearchResponse


# 楽天レシピAPIを使用してレシピを検索するサービス
class RakutenRecipeService:
    def __init__(self) -> None:
        # 設定を取得する
        self.settings = get_settings()


    # パラメータを作成する
    def build_params(self) -> dict:
        params = {
            "applicationId": self.settings.rakuten_app_id,
            "categoryId": self.settings.rakuten_category_id,
            "format": "json",
        }
        return params


    # 楽天レシピAPIを使用してレシピをlimit件数分検索する
    async def search(
        self,
        ingredient: str,
        limit: int = 10
    ) -> list[RecipeSearchResponse]:
        if not self.settings.rakuten_app_id:
            return []

        # パラメータを作成する
        params = self.build_params()

        if self.settings.rakuten_affiliate_id:
            params["affiliateId"] = self.settings.rakuten_affiliate_id

        # 楽天レシピAPIを使用してレシピを検索する
        async with httpx.AsyncClient(timeout=15.0) as client:
            response = await client.get(self.settings.rakuten_url, params=params)
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

