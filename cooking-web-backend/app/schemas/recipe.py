from pydantic import BaseModel, Field


class RecipeSearchResponse(BaseModel):
    recipe_id: str
    title: str
    description: str
    url: str
    image_url: str | None = None
    materials: list[str] = Field(default_factory=list)


class RecipeSearchResult(BaseModel):
    source: str
    total: int
    items: list[RecipeSearchResponse]
