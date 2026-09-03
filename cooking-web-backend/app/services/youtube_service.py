# !/usr/bin/env python
# -*- coding: utf-8 -*-

import httpx

from app.core.config import get_settings
from app.schemas.recipe import YouTubeVideoResponse
from app.services.logger import get_logger

YOUTUBE_SEARCH_URL = get_settings().youtube_search_url


# YouTube Data API v3 を使用してレシピ動画を検索するサービス
class YouTubeRecipeService:
    def __init__(self) -> None:
        """ コンストラクタ """
        self.settings = get_settings() # 設定を取得する
        self.logger = get_logger(__name__) # ログを取得する


    async def search_for_recipes_by_youtube(self, ingredient: str, limit: int = 5) -> list[YouTubeVideoResponse]:
        """
        YouTube Data API v3 を使用して食材からレシピ動画を検索する
        """

        # APIキーの設定を検証する
        if not self.validate_youtube_settings():
            return []

        # パラメータを設定する
        params = {
            "key": self.settings.youtube_api_key,
            "q": f"{ingredient} レシピ",
            "part": "snippet",
            "type": "video",
            "maxResults": limit,
        }

        try:
            async with httpx.AsyncClient(timeout=15.0) as client:
                response = await client.get(YOUTUBE_SEARCH_URL, params=params)
                response.raise_for_status()
                payload = response.json()
        except httpx.HTTPError as exc:
            self.logger.error(f"YouTube動画検索エラー: {exc}")
            return []

        # レシピ動画の結果を整形する
        result: list[YouTubeVideoResponse] = []
        for item in payload.get("items", []):
            video_id = item.get("id", {}).get("videoId", "")
            snippet = item.get("snippet", {})
            result.append(
                YouTubeVideoResponse(
                    video_id=video_id,
                    title=snippet.get("title", ""),
                    description=snippet.get("description", ""),
                    url=f"https://www.youtube.com/watch?v={video_id}",
                    thumbnail_url=snippet.get("thumbnails", {}).get("medium", {}).get("url"),
                )
            )
        return result


    def validate_youtube_settings(self) -> bool:
        """
        APIキーの設定を検証する
        """
        if not self.settings.youtube_api_key:
            self.logger.error("YouTube Data API v3 のキーが空です")
            return False

        self.logger.info("YouTube Data API v3 の設定が正常に設定されています")
        return True
