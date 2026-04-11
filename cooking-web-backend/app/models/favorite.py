# !/usr/bin/env python
# -*- coding: utf-8 -*-


from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

# お気に入りレシピモデル
class FavoriteRecipe(Base):
    __tablename__ = "favorite_recipes"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    recipe_id: Mapped[str] = mapped_column(String(50), nullable=False)
    recipe_title: Mapped[str] = mapped_column(String(255), nullable=False)
    recipe_url: Mapped[str] = mapped_column(String(500), nullable=False)
    recipe_image_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

    user = relationship("User", back_populates="favorites")
