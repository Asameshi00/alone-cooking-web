from app.api.ai import router as ai_router
from app.api.favorites import router as favorites_router
from app.api.health import router as health_router
from app.api.inventory import router as inventory_router
from app.api.recipes import router as recipes_router

__all__ = [
    "health_router",
    "recipes_router",
    "ai_router",
    "inventory_router",
    "favorites_router",
]
