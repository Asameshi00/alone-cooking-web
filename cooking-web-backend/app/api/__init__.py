# !/usr/bin/env python
# -*- coding: utf-8 -*-

""" __init__.py """

from app.api.board import router as board_router
from app.api.favorites import router as favorites_router
from app.api.health import router as health_router
from app.api.inventory import router as inventory_router

__all__ = [
    "board_router",
    "health_router",
    "inventory_router",
    "favorites_router",
]
