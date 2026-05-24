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
    _category_df: pd.DataFrame | None = None  # 起動後に一度だけ取得するクラスレベルキャッシュ

    def __init__(self) -> None:
        """ コンストラクタ """
        self.logger = get_logger(__name__)
        self.settings = get_settings()


    def build_category_df(self, json_data: dict) -> pd.DataFrame:
        """
        APIレスポンスからカテゴリDFを構築する（大・中・小すべて含む）

        Args:
            json_data (dict): 検索結果のレスポンスデータ

        Returns:
            pd.DataFrame: 整形されたデータフレーム
        """
        parent_dict: dict[str, str] = {}
        rows: list[dict] = []

        # 小カテゴリ
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

        # 大カテゴリ
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


    async def fetch_category_df(self, client: httpx.AsyncClient) -> pd.DataFrame:
        """
        カテゴリ一覧を取得してDFにキャッシュする

        Args:
            client (httpx.AsyncClient): HTTPクライアント

        Returns:
            pd.DataFrame: 整形されたデータフレーム
        """
        if RakutenRecipeService._category_df is not None:
            return RakutenRecipeService._category_df

        # リクエストを投げてレスポンスを受け取る
        params = {
            "applicationId": self.settings.rakuten_app_id,
            "format": "json"
        }
        response = await client.get(CATEGORY_LIST_URL, params=params)
        response.raise_for_status()

        # レスポンスをもとにデータフレームを整形する
        df = self.build_category_df(response.json())
        RakutenRecipeService._category_df = df
        self.logger.info(f"カテゴリDF構築完了: {len(df)}件")
        return df


    async def map_category_id(self, ingredient: str, client: httpx.AsyncClient) -> str | None:
        """
        食材名からカテゴリIDをマッピングさせる

        Args:
            ingredient (str): 食材名
            client (httpx.AsyncClient): クライアント

        Returns:
            str | None: _description_
        """
        df = await self.fetch_category_df(client)
        matched = df[df["categoryName"].str.contains(ingredient, na=False)]
        if matched.empty:
            self.logger.warning(f"カテゴリが見つかりませんでした: {ingredient}")
            return None
        return str(matched.iloc[0]["categoryId"])


    async def search_for_recipes(self, ingredient: str, limit: int = 10) -> list[RakutenRecipeSearchResponse]:
        """
        食材からレシピ検索を行う

        Args:
            ingredient (str): _description_
            limit (int, optional): _description_. Defaults to 10.

        Returns:
            list[RakutenRecipeSearchResponse]: _description_
        """
        if not self.settings.rakuten_app_id:
            self.logger.error("楽天ApplicationAPIが空です")
            return []

        async with httpx.AsyncClient(timeout=15.0) as client:
            # 食材とカテゴリIDをマッピングする
            category_id = await self.map_category_id(ingredient, client)
            if category_id is None:
                self.logger.warning("食材に対応するカテゴリIDがありませんでした")
                return []

            params: dict = {
                "applicationId": self.settings.rakuten_app_id,
                "categoryId": category_id,
                "format": "json",
            }
            if self.settings.rakuten_affiliate_id is None:
                self.logger.error("楽天AffiliateIDがありません")
                return []
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
