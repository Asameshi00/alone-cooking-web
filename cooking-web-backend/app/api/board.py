# !/usr/bin/env python
# -*- coding: utf-8 -*-


from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import db_session_dep
from app.schemas.board import BoardIngredientsRequest, BoardIngredientsResponse, BoardSearchRequest
from app.schemas.recipe import BoardRecipeSearchResponse
from app.services.board_service import BoardService

board_service = BoardService()
router = APIRouter(prefix="/board", tags=["board"])


# inventory_ids から検索にかける食材一覧（board）を取得するエンドポイント
@router.post("/ingredients", response_model=BoardIngredientsResponse)
async def get_board_ingredients(
    payload: BoardIngredientsRequest,
    session: AsyncSession = Depends(db_session_dep),
) -> BoardIngredientsResponse:
    try:
        names = await board_service.fetch_ingredient_names(
            session=session,
            user_id=payload.user_id,
            inventory_ids=payload.inventory_ids,
        )
    except ValueError:
        raise HTTPException(status_code=404, detail="在庫が見つかりません")
    return BoardIngredientsResponse(ingredient_names=names)


# まな板にある食材からレシピを検索するエンドポイント
@router.post("/search", response_model=BoardRecipeSearchResponse)
async def search_recipes_from_board(
    payload: BoardSearchRequest,
) -> BoardRecipeSearchResponse:
    results = await board_service.search_recipes_from_board(
        ingredient_names=payload.ingredient_names,
        limit=payload.limit,
    )
    return BoardRecipeSearchResponse(results=results)
