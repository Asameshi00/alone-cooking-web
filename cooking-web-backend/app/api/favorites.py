# !/usr/bin/env python
# -*- coding: utf-8 -*-


from fastapi import APIRouter, Depends, Query
from sqlalchemy import Select, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import db_session_dep
from app.models.favorite_model import FavoriteRecipe
from app.schemas.favorite import FavoriteCreate, FavoriteResponse

router = APIRouter(prefix="/recipes/favorites", tags=["favorites"])

# お気に入りレシピを取得する
@router.get("", response_model=list[FavoriteResponse])
async def list_favorites(
    user_id: int = Query(..., ge=1),
    session: AsyncSession = Depends(db_session_dep),
) -> list[FavoriteResponse]:
    stmt: Select[tuple[FavoriteRecipe]] = select(FavoriteRecipe).where(FavoriteRecipe.user_id == user_id)
    rows = (await session.execute(stmt)).scalars().all()
    return [FavoriteResponse.model_validate(row) for row in rows]


# お気に入りレシピを作成する
@router.post("", response_model=FavoriteResponse)
async def create_favorite(
    payload: FavoriteCreate,
    session: AsyncSession = Depends(db_session_dep),
) -> FavoriteResponse:
    item = FavoriteRecipe(**payload.model_dump())
    session.add(item)
    await session.commit()
    await session.refresh(item)
    return FavoriteResponse.model_validate(item)
