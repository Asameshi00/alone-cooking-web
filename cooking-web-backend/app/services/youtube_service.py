# !/usr/bin/env python
# -*- coding: utf-8 -*-

import httpx

from app.core.config import get_settings
from app.schemas.recipe import YouTubeVideoResponse

YOUTUBE_SEARCH_URL = "https://www.googleapis.com/youtube/v3/search"


# YouTube Data API v3 を使用してレシピ動画を検索するサービス
class YouTubeRecipeService:
    def __init__(self) -> None:
        self.settings = get_settings()

    async def search(self, ingredient: str, limit: int = 5) -> list[YouTubeVideoResponse]:
        if not self.settings.youtube_api_key:
            return []

        params = {
            "key": self.settings.youtube_api_key,
            "q": f"{ingredient} レシピ",
            "part": "snippet",
            "type": "video",
            "maxResults": limit,
        }

        async with httpx.AsyncClient(timeout=15.0) as client:
            response = await client.get(YOUTUBE_SEARCH_URL, params=params)
            response.raise_for_status()
            payload = response.json()

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
