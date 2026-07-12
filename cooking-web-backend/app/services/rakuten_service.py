# !/usr/bin/env python
# -*- coding: utf-8 -*-

import httpx
import pandas as pd

from app.core.config import get_settings
from app.schemas.recipe import RakutenRecipeSearchResponse
from app.services.logger import get_logger

CATEGORY_LIST_URL = "https://app.rakuten.co.jp/services/api/Recipe/CategoryList/20170426"
CATEGORY_RANKING_URL = "https://app.rakuten.co.jp/services/api/Recipe/CategoryRanking/20170426"


class RakutenRecipeService:
    _category_df: pd.DataFrame | None = None # 起動後に一度だけ取得するクラスレベルキャッシュ

    def __init__(self) -> None:
        """ コンストラクタ """
        self.logger = get_logger(__name__) # ログを取得する
        self.settings = get_settings() # 設定を取得する

    async def search_for_recipes_by_rakuten(self, ingredient: str, limit: int = 10) -> list[RakutenRecipeSearchResponse]:
        """
        食材からレシピ検索を行う
        """

        # APIとAffiliateIDの設定を検証する
        if not self.validate_rakuten_settings():
            return []

        async with httpx.AsyncClient(timeout=15.0) as client:
            # 食材とカテゴリIDをマッピングする
            category_id = await self.map_category_id_from_ingredient(ingredient, client)

            params: dict = {
                "applicationId": self.settings.rakuten_app_id,
                "categoryId": category_id,
                "format": "json",
            }

            params["affiliateId"] = self.settings.rakuten_affiliate_id

            response = await client.get(CATEGORY_RANKING_URL, params=params)
            response.raise_for_status()
            payload = response.json()

        # レシピの結果を整形する
        result: list[RakutenRecipeSearchResponse] = []
        for item in payload.get("result", [])[:limit]:
            result.append(
                RakutenRecipeSearchResponse(
                    recipe_id=str(item.get("recipeId", "")),
                    title=item.get("recipeTitle", ""),
                    description=item.get("recipeDescription", ""),
                    url=item.get("recipeUrl", ""),
                    image_url=item.get("foodImageUrl"),
                    materials=item.get("recipeMaterial", []),
                )
            )
        return result


    async def map_category_id_from_ingredient(self, ingredient: str, client: httpx.AsyncClient) -> str | None:
        """
        食材名からカテゴリIDをマッピングさせる
        """
        df = await self.fetch_category_dataframe(client) # カテゴリ一覧を取得する
        matched = df[df["categoryName"].str.contains(ingredient, na=False)]
        if matched.empty:
            self.logger.warning(f"カテゴリが見つかりませんでした: {ingredient}")
            return None

        # カテゴリIDを返す
        return str(matched.iloc[0]["categoryId"])


    async def fetch_category_dataframe(self, client: httpx.AsyncClient) -> pd.DataFrame:
        """
        カテゴリ一覧を取得してデータフレームにキャッシュする
        """
        if RakutenRecipeService._category_df is not None:
            return RakutenRecipeService._category_df

        # カテゴリ一覧を取得する
        params: dict = {
            "applicationId": self.settings.rakuten_app_id,
            "format": "json",
        }
        response = await client.get(CATEGORY_LIST_URL, params=params)
        response.raise_for_status() # レスポンスを検証する
        json_data = response.json() # レスポンスをJSON形式に変換する
        df = self.build_category_dataframe(json_data)
        RakutenRecipeService._category_df = df
        return df


    def build_category_dataframe(self, json_data: dict) -> pd.DataFrame:
        """
        APIレスポンスからカテゴリデータフレームを構築する（大・中・小すべて含む）
        """
        parent_dict: dict[str, str] = {}
        rows: list[dict] = []

        # 大カテゴリ
        for cat in json_data["result"]["large"]:
            rows.append({
                "category1": str(cat["categoryId"]),
                "category2": "",
                "category3": "",
                "categoryId": str(cat["categoryId"]),
                "categoryName": cat["categoryName"],
            })

        # 中カテゴリ
        for cat in json_data["result"]["medium"]:
            parent_dict[str(cat["categoryId"])] = str(cat["parentCategoryId"])
            rows.append({
                "category1": str(cat["parentCategoryId"]),
                "category2": str(cat["categoryId"]),
                "category3": "",
                "categoryId": f"{cat['parentCategoryId']}-{cat['categoryId']}",
                "categoryName": cat["categoryName"],
            })

        # 小カテゴリ
        for cat in json_data["result"]["small"]:
            parent_id = str(cat["parentCategoryId"])
            grandparent_id = parent_dict.get(parent_id, "")
            rows.append({
                "category1": grandparent_id,
                "category2": parent_id,
                "category3": str(cat["categoryId"]),
                "categoryId": f"{grandparent_id}-{parent_id}-{cat['categoryId']}",
                "categoryName": cat["categoryName"],
            })

        return pd.DataFrame(rows, columns=["category1", "category2", "category3", "categoryId", "categoryName"])


    def validate_rakuten_settings(self) -> bool:
        """
        APIとAffiliateIDの設定を検証する
        """
        if not self.settings.rakuten_app_id:
            self.logger.error("楽天ApplicationAPIが空です")
            return False

        if not self.settings.rakuten_affiliate_id:
            self.logger.error("楽天AffiliateIDが空です")
            return False

        self.logger.info("楽天設定が正常に設定されています")
        return True
