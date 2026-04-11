# !/usr/bin/env python
# -*- coding: utf-8 -*-


from fastapi import APIRouter

router = APIRouter(prefix="/health", tags=["health"])

# health checkを確認するエンドポイント
@router.get("")
async def health_check() -> dict[str, str]:
    return {"status": "ok"}
