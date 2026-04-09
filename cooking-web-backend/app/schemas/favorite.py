from datetime import datetime

from pydantic import BaseModel, Field

from app.schemas.common import ORMBase


class FavoriteCreate(BaseModel):
    user_id: int = Field(..., ge=1)
    recipe_id: str = Field(..., min_length=1, max_length=50)
    recipe_title: str = Field(..., min_length=1, max_length=255)
    recipe_url: str = Field(..., min_length=1, max_length=500)
    recipe_image_url: str | None = Field(default=None, max_length=500)


class FavoriteResponse(ORMBase):
    id: int
    user_id: int
    recipe_id: str
    recipe_title: str
    recipe_url: str
    recipe_image_url: str | None
    created_at: datetime
