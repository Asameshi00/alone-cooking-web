# !/usr/bin/env python
# -*- coding: utf-8 -*-


from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

# お気に入りレシピモデル
class FavoriteRecipe(Base):
    # テーブル名
    __tablename__ = "favorite_recipes"

    # 主キー
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    # ユーザーID
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    # レシピID
    recipe_id: Mapped[str] = mapped_column(String(50), nullable=False)
    # レシピタイトル
    recipe_title: Mapped[str] = mapped_column(String(255), nullable=False)
    # レシピURL
    recipe_url: Mapped[str] = mapped_column(String(500), nullable=False)
    # レシピ画像URL
    recipe_image_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    # 作成日時
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

    # ユーザーとの関係を定義
    # お気に入りレシピはユーザーに属する
    user = relationship("User", back_populates="favorites")
