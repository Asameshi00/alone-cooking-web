# !/usr/bin/env python
# -*- coding: utf-8 -*-

from functools import lru_cache

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

# 設定ファイル
class Settings(BaseSettings):
    MODEL_CONFIG = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    APP_NAME: str = "Cooking Web Backend" # アプリケーション名
    APP_ENV: str = "dev" # アプリケーション環境
    API_PREFIX: str = "/api/v1" # APIのプレフィックス

    DATABASE_URL: str = "sqlite+aiosqlite:///./app.db" # データベースのURL

    ALLOWED_ORIGINS: list[str] = ["http://localhost:5173", "http://127.0.0.1:5173"] # 許可するオリジン

    RAKUTEN_APP_ID: str | None = None # 楽天レシピAPIのアプリID
    RAKUTEN_AFFILIATE_ID: str | None = None # 楽天レシピAPIのアフィリエイトID
    RAKUTEN_CATEGORY_ID: str = "14-121" # 楽天レシピAPIのカテゴリID

    AI_PROVIDER: str = "local" # AIのプロバイダ
    OPENAI_API_KEY: str | None = None # OpenAIのAPIキー
    OPENAI_MODEL: str = "gpt-4o-mini" # OpenAIのモデル
    GEMINI_API_KEY: str | None = None # GeminiのAPIキー
    GEMINI_MODEL: str = "gemini-1.5-flash" # Geminiのモデル

    @field_validator("ALLOWED_ORIGINS", mode="before")
    @classmethod
    def parse_allowed_origins(cls, value: str | list[str]) -> list[str]:
        if isinstance(value, list):
            return value
        return [v.strip() for v in value.split(",") if v.strip()]


# 設定ファイルを取得する
@lru_cache
def get_settings() -> Settings:
    return Settings()
