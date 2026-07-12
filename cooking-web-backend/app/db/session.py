# !/usr/bin/env python
# -*- coding: utf-8 -*-


from collections.abc import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from app.core.config import get_settings

# 設定ファイルを取得する
settings = get_settings()

# データベースエンジンを作成する
engine = create_async_engine(settings.database_url, echo=settings.app_env == "dev")
SessionLocal = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

# データベースセッションを取得する
async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as session:
        yield session
