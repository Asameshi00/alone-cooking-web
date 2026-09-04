# !/usr/bin/env python
# -*- coding: utf-8 -*-


from datetime import datetime

from sqlalchemy import DateTime, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

# ユーザーモデル
class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

    inventories = relationship("InventoryItem", back_populates="user", cascade="all,delete")
    favorites = relationship("Favorite", back_populates="user", cascade="all,delete")
