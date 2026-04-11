# !/usr/bin/env python
# -*- coding: utf-8 -*-


from collections.abc import AsyncGenerator

from app.db.session import get_db_session

# データベースセッションを取得する
async def db_session_dep() -> AsyncGenerator:
    async for session in get_db_session():
        yield session
