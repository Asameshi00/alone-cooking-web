from fastapi import APIRouter, Depends, Query
from sqlalchemy import Select, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import db_session_dep
from app.models.favorite import FavoriteRecipe
from app.schemas.favorite import FavoriteCreate, FavoriteResponse

router = APIRouter(prefix="/favorites", tags=["favorites"])


@router.get("", response_model=list[FavoriteResponse])
async def list_favorites(
    user_id: int = Query(..., ge=1),
    session: AsyncSession = Depends(db_session_dep),
) -> list[FavoriteResponse]:
    stmt: Select[tuple[FavoriteRecipe]] = select(FavoriteRecipe).where(FavoriteRecipe.user_id == user_id)
    rows = (await session.execute(stmt)).scalars().all()
    return [FavoriteResponse.model_validate(row) for row in rows]


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
