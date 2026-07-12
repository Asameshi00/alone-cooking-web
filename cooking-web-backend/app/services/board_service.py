# !/usr/bin/env python
# -*- coding: utf-8 -*-

import asyncio

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.inventory_model import InventoryItem
from app.schemas.recipe import RecipeSearchResult
from app.services.logger import get_logger
from app.services.rakuten_service import RakutenRecipeService
from app.services.youtube_service import YouTubeRecipeService


# まな板のサービス
class BoardService:

    def __init__(self) -> None:
        self.logger = get_logger(__name__) # ログを取得
        self._rakuten_service = RakutenRecipeService() # 楽天レシピの取得
        self._youtube_service = YouTubeRecipeService() # YouTube動画の取得

    # まな板の食材名一覧からレシピを検索する
    async def search_recipes_from_board(
        self,
        ingredient_names: list[str],
        limit: int,
    ) -> list[RecipeSearchResult]:
        results = await asyncio.gather(*[
            self.search_recipes_for_ingredient(ingredient=name, limit=limit)
            for name in ingredient_names
        ])
        self.logger.info(f"まな板からのレシピ検索完了: ingredients={ingredient_names}")
        return list(results)


    # 食材idから食材名に変更
    async def fetch_ingredient_names(
        self,
        session: AsyncSession,
        user_id: int,
        inventory_ids: list[int],
    ) -> list[str]:
        stmt = (
            select(InventoryItem.ingredient_name)
            .where(InventoryItem.user_id == user_id)
            .where(InventoryItem.id.in_(inventory_ids))
        )
        names = list((await session.execute(stmt)).scalars().all())
        if not names:
            raise ValueError(f"在庫が見つかりません: user_id={user_id}, inventory_ids={inventory_ids}")
        self.logger.info(f"食材名を取得しました: user_id={user_id}, count={len(names)}")
        return names


    # 食材名を使ってレシピ検索を行う
    async def search_recipes_for_ingredient(
        self, ingredient: str, limit: int
    ) -> RecipeSearchResult:
        rakuten_recipes, youtube_videos = await asyncio.gather(
            self._rakuten_service.search_for_recipes_by_rakuten(ingredient=ingredient, limit=limit),
            self._youtube_service.search_for_recipes_by_youtube(ingredient=ingredient, limit=limit),
        )
        return RecipeSearchResult(
            ingredient=ingredient,
            rakuten_recipes=rakuten_recipes,
            youtube_videos=youtube_videos,
        )
