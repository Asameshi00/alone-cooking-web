# !/usr/bin/env python
# -*- coding: utf-8 -*-


from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import db_session_dep
from app.schemas.favorite import FavoriteRequest, FavoriteKind, FavoriteResponse
from app.services.favorite_service import FavoriteService

favorite_service = FavoriteService()
router = APIRouter(prefix="/recipes/favorites", tags=["favorites"])

# お気に入りを取得する
@router.get("", response_model=list[FavoriteResponse])
async def list_favorites(
    user_id: int = Query(..., ge=1),
    session: AsyncSession = Depends(db_session_dep),
) -> list[FavoriteResponse]:
    items = await favorite_service.list_favorites(session=session, user_id=user_id)
    return [FavoriteResponse.model_validate(item) for item in items]


# お気に入りを作成する
@router.post("", response_model=FavoriteResponse)
async def create_favorite(
    payload: FavoriteRequest,
    session: AsyncSession = Depends(db_session_dep),
) -> FavoriteResponse:
    item = await favorite_service.create_favorite(
        session=session,
        user_id=payload.user_id,
        kind=payload.kind.value,
        item_id=payload.item_id,
        title=payload.title,
        description=payload.description,
        url=payload.url,
        image_url=payload.image_url,
    )
    return FavoriteResponse.model_validate(item)


# お気に入りを削除する
@router.delete("", status_code=204)
async def delete_favorite(
    user_id: int = Query(..., ge=1),
    item_id: str = Query(..., min_length=1),
    kind: FavoriteKind = Query(...),
    session: AsyncSession = Depends(db_session_dep),
) -> None:
    try:
        await favorite_service.delete_favorite(session=session, user_id=user_id, item_id=item_id, kind=kind.value)
    except ValueError:
        raise HTTPException(status_code=404, detail="お気に入りが見つかりません")
