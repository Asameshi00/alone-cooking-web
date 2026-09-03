# !/usr/bin/env python
# -*- coding: utf-8 -*-


from functools import lru_cache

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    設定クラス
    """

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_name: str = "Cooking Web Backend" # アプリケーション名
    app_env: str = "dev" # アプリケーション環境
    api_prefix: str = "/api/v1" # APIのプレフィックス

    database_url: str = "sqlite+aiosqlite:///./app.db" # データベースのURL

    allowed_origins: list[str] = ["http://localhost:5173", "http://127.0.0.1:5173"] # 許可するオリジン

    rakuten_app_id: str | None = None # 楽天レシピAPIのアプリID
    rakuten_affiliate_id: str | None = None # 楽天レシピAPIのアフィリエイトID

    youtube_api_key: str | None = None # YouTube Data API キー

    # エンドポイントのURL
    rakuten_category_list_url: str = "https://app.rakuten.co.jp/services/api/Recipe/CategoryList/20170426"
    rakuten_category_ranking_url: str = "https://app.rakuten.co.jp/services/api/Recipe/CategoryRanking/20170426"
    youtube_search_url: str = "https://www.googleapis.com/youtube/v3/search"

    @field_validator("allowed_origins", mode="before")
    @classmethod
    def parse_allowed_origins(cls, value: str | list[str]) -> list[str]:
        if isinstance(value, list):
            return value
        return [v.strip() for v in value.split(",") if v.strip()]


# 設定ファイルを取得する
@lru_cache
def get_settings() -> Settings:
    return Settings()
