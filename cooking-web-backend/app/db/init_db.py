# !/usr/bin/env python
# -*- coding: utf-8 -*-


from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.base import Base
from app.db.session import engine
from app.models import User

# データベースを初期化する
async def init_db() -> None:
    # データベースを初期化する
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # データベースセッションを取得する
    async with AsyncSession(engine, expire_on_commit=False) as session:
        # ユーザーを取得する
        result = await session.execute(select(User).where(User.email == "demo@example.com"))
        demo_user = result.scalar_one_or_none()
        #  ユーザーが存在しない場合は作成する
        if demo_user is None:
            session.add(User(name="Demo User", email="demo@example.com"))
            await session.commit()
