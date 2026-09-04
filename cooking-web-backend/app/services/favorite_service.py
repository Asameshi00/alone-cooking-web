# !/usr/bin/env python
# -*- coding: utf-8 -*-


from sqlalchemy import Select, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.favorite_model import Favorite
from app.services.logger import get_logger


class FavoriteService:
    """ お気に入りサービスクラス """

    def __init__(self) -> None:
        """ コンストラクタ """
        self.logger = get_logger(__name__)

    # お気に入りを取得する
    async def list_favorites(self, session: AsyncSession, user_id: int) -> list[Favorite]:
        stmt: Select[tuple[Favorite]] = select(Favorite).where(Favorite.user_id == user_id)
        items = list((await session.execute(stmt)).scalars().all())
        self.logger.info(f"お気に入りを取得しました: user_id={user_id}, count={len(items)}")
        return items


    # お気に入りを作成する（既に登録済みの場合はそのまま返す）
    async def create_favorite(
        self,
        session: AsyncSession,
        *,
        user_id: int,
        kind: str,
        item_id: str,
        title: str,
        description: str | None,
        url: str,
        image_url: str | None,
    ) -> Favorite:
        existing = await self._find_favorite(session, user_id=user_id, item_id=item_id, kind=kind)
        if existing is not None:
            self.logger.info(f"お気に入りは既に登録されています: user_id={user_id}, item_id={item_id}, kind={kind}")
            return existing

        item = Favorite(
            user_id=user_id,
            kind=kind,
            item_id=item_id,
            title=title,
            description=description,
            url=url,
            image_url=image_url,
        )
        session.add(item)
        await session.commit()
        await session.refresh(item)
        self.logger.info(f"お気に入りを登録しました: user_id={user_id}, item_id={item_id}, kind={kind}")
        return item


    # お気に入りを削除する
    async def delete_favorite(self, session: AsyncSession, *, user_id: int, item_id: str, kind: str) -> None:
        item = await self._find_favorite(session, user_id=user_id, item_id=item_id, kind=kind)
        if item is None:
            raise ValueError(f"お気に入りが見つかりません: user_id={user_id}, item_id={item_id}, kind={kind}")

        await session.delete(item)
        await session.commit()
        self.logger.info(f"お気に入りを削除しました: user_id={user_id}, item_id={item_id}, kind={kind}")


    # user_id・item_id・kindでお気に入りを検索する
    async def _find_favorite(self, session: AsyncSession, *, user_id: int, item_id: str, kind: str) -> Favorite | None:
        stmt: Select[tuple[Favorite]] = select(Favorite).where(
            Favorite.user_id == user_id,
            Favorite.item_id == item_id,
            Favorite.kind == kind,
        )
        return (await session.execute(stmt)).scalar_one_or_none()
