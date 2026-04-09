from pydantic import BaseModel, Field


class AISuggestionRequest(BaseModel):
    leftovers: list[str] = Field(default_factory=list)
    bargain_items: list[str] = Field(default_factory=list)


class AISuggestionResponse(BaseModel):
    provider: str
    recipe_title: str
    recipe_description: str
    steps: list[str]
    tips: list[str]
