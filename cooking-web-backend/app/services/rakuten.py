import httpx

from app.core.config import get_settings
from app.schemas.recipe import RecipeSearchResponse

RAKUTEN_SEARCH_URL = "https://app.rakuten.co.jp/services/api/Recipe/CategoryRanking/20170426"


class RakutenRecipeService:
    def __init__(self) -> None:
        self.settings = get_settings()

    async def search(self, ingredient: str, limit: int = 10) -> list[RecipeSearchResponse]:
        if not self.settings.rakuten_app_id:
            return self._fallback(ingredient, limit)

        params = {
            "applicationId": self.settings.rakuten_app_id,
            "categoryId": self.settings.rakuten_category_id,
            "format": "json",
        }
        if self.settings.rakuten_affiliate_id:
            params["affiliateId"] = self.settings.rakuten_affiliate_id

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
