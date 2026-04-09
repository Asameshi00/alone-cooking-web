from fastapi import APIRouter

from app.schemas.ai import AISuggestionRequest, AISuggestionResponse
from app.services.ai import AIRecipeService

router = APIRouter(prefix="/ai", tags=["ai"])
service = AIRecipeService()


@router.post("/suggest", response_model=AISuggestionResponse)
async def suggest_recipe(payload: AISuggestionRequest) -> AISuggestionResponse:
    return await service.suggest(payload)
