# !/usr/bin/env python
# -*- coding: utf-8 -*-

from functools import lru_cache

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

# 設定ファイル
class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_name: str = "Cooking Web Backend" # アプリケーション名
    app_env: str = "dev" # アプリケーション環境
    api_prefix: str = "/api/v1" # APIのプレフィックス

    database_url: str = "sqlite+aiosqlite:///./app.db" # データベースのURL

    allowed_origins: list[str] = ["http://localhost:5173", "http://127.0.0.1:5173"] # 許可するオリジン

    rakuten_app_id: str | None = None # 楽天レシピAPIのアプリID
    rakuten_affiliate_id: str | None = None # 楽天レシピAPIのアフィリエイトID
    rakuten_category_id: str = "14-121" # 楽天レシピAPIのカテゴリID

    ai_provider: str = "local" # AIのプロバイダ
    openai_api_key: str | None = None # OpenAIのAPIキー
    openai_model: str = "gpt-4o-mini" # OpenAIのモデル
    gemini_api_key: str | None = None # GeminiのAPIキー
    gemini_model: str = "gemini-1.5-flash" # Geminiのモデル

    @field_validator("allowed_origins", mode="before")
    @classmethod
    def parse_origins(cls, value: str | list[str]) -> list[str]:
        if isinstance(value, list):
            return value
        return [v.strip() for v in value.split(",") if v.strip()]


# 設定ファイルを取得する
@lru_cache
def get_settings() -> Settings:
    return Settings()
